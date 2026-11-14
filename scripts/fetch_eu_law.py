#!/usr/bin/env python3
"""Fetch EU legal texts from Cellar and check the book's article references.

Why this script exists: ``eur-lex.europa.eu`` serves a JavaScript loader to
automated clients, so the text of an article cannot be read from it. The
Publications Office's Cellar service (``publications.europa.eu``) is the
repository EUR-Lex is built on. It returns the authentic text as XHTML when the
request names the CELEX number and asks for ``application/xhtml+xml``. This
script wraps that.

Commands::

    python3 scripts/fetch_eu_law.py list
    python3 scripts/fetch_eu_law.py get gdpr --article 35
    python3 scripts/fetch_eu_law.py get ai_act --article 4 --paragraph 1
    python3 scripts/fetch_eu_law.py get ai_act --recital 1
    python3 scripts/fetch_eu_law.py get 32024R2847 --toc
    python3 scripts/fetch_eu_law.py latest 32024R1689      # consolidated versions (SPARQL)
    python3 scripts/fetch_eu_law.py sync                   # download every instrument, write the manifest
    python3 scripts/fetch_eu_law.py check                  # article references in docs/*.md against the texts
    python3 scripts/fetch_eu_law.py check --report out.md  # the same, as a Markdown report

Swedish statutes (the Riksdag's SFS database, plain text with chapter and section headings)::

    python3 scripts/fetch_eu_law.py sfs list
    python3 scripts/fetch_eu_law.py sfs get forvaltningslag --section 2
    python3 scripts/fetch_eu_law.py sfs get kommunallag --chapter 6 --section 37
    python3 scripts/fetch_eu_law.py sfs sync
    python3 scripts/fetch_eu_law.py sfs check --report sfs.md

Texts are cached in ``data/law/`` (XHTML is git-ignored; ``data/law/manifest.json``
records CELEX, language, retrieval date and SHA-256 and is committed). Only the
standard library is used. ``check`` verifies that a cited article exists and shows
its title and first words; it does not judge whether the sentence in the chapter
is right. That comparison is the reviewer's, with the text this script prints.

Authority: a text fetched here is the text published in the Official Journal (or
the consolidated text, which has no legal effect itself and is marked as such by
the Publications Office). Cite the Official Journal reference in the bibliography.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAW = ROOT / "data" / "law"
MANIFEST = LAW / "manifest.json"
DOCS = ROOT / "docs"
XH = "{http://www.w3.org/1999/xhtml}"
CELLAR = "https://publications.europa.eu/resource/celex/"
SPARQL = "https://publications.europa.eu/webapi/rdf/sparql"
LANG = "eng"

# key -> (CELEX, short name, aliases used in the manuscript to recognise a reference)
INSTRUMENTS: dict[str, tuple[str, str, list[str]]] = {
    "gdpr": ("32016R0679", "Regulation (EU) 2016/679 (GDPR)", ["GDPR", "General Data Protection Regulation", "Regulation (EU) 2016/679"]),
    # Consolidated text as amended by Regulation (EU) 2026/1744 (documentary, no legal effect of its own);
    # the text as originally adopted is "ai_act_base". Re-run `latest 32024R1689` to see newer consolidations.
    "ai_act": ("02024R1689-20260727", "Regulation (EU) 2024/1689 (AI Act), consolidated 2026-07-27", ["AI Act", "Artificial Intelligence Act", "Regulation (EU) 2024/1689"]),
    "ai_act_base": ("32024R1689", "Regulation (EU) 2024/1689 (AI Act), as adopted", []),
    "ai_omnibus": ("32026R1744", "Regulation (EU) 2026/1744 (AI Act simplification)", ["Regulation (EU) 2026/1744", "Digital Omnibus"]),
    "dora": ("32022R2554", "Regulation (EU) 2022/2554 (DORA)", ["DORA", "Regulation (EU) 2022/2554"]),
    "dora_rts_ict": ("32024R1774", "Delegated Regulation (EU) 2024/1774", ["Regulation (EU) 2024/1774", "Delegated Regulation (EU) 2024/1774"]),
    "nis2": ("32022L2555", "Directive (EU) 2022/2555 (NIS 2)", ["NIS 2", "NIS2", "Directive (EU) 2022/2555"]),
    "cra": ("32024R2847", "Regulation (EU) 2024/2847 (Cyber Resilience Act)", ["Cyber Resilience Act", "CRA", "Regulation (EU) 2024/2847"]),
    "pld": ("32024L2853", "Directive (EU) 2024/2853 (Product Liability Directive)", ["Product Liability Directive", "Directive (EU) 2024/2853"]),
    "web_accessibility": ("32016L2102", "Directive (EU) 2016/2102 (Web Accessibility Directive)", ["Web Accessibility Directive", "Directive (EU) 2016/2102"]),
    "eaa": ("32019L0882", "Directive (EU) 2019/882 (European Accessibility Act)", ["European Accessibility Act", "Directive (EU) 2019/882"]),
    "procurement": ("02014L0024-20260101", "Directive 2014/24/EU (public procurement), consolidated 2026-01-01", ["Directive 2014/24/EU", "public procurement directive"]),
    "data_act": ("32023R2854", "Regulation (EU) 2023/2854 (Data Act)", ["Data Act", "Regulation (EU) 2023/2854"]),
    "software_directive": ("32009L0024", "Directive 2009/24/EC (legal protection of computer programs)", ["Directive 2009/24/EC", "Software Directive"]),
    "dsm_copyright": ("32019L0790", "Directive (EU) 2019/790 (Copyright in the Digital Single Market)", ["Directive (EU) 2019/790", "DSM Directive"]),
}
BY_CELEX = {v[0]: k for k, v in INSTRUMENTS.items()}


# ---------------------------------------------------------------- fetching
def _request(url: str, accept: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers={"Accept": accept, "Accept-Language": LANG,
                                               "User-Agent": "book-source-check/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # honours HTTPS_PROXY
        return resp.read()


def resolve(key_or_celex: str) -> str:
    return INSTRUMENTS[key_or_celex][0] if key_or_celex in INSTRUMENTS else key_or_celex


def cache_path(celex: str) -> Path:
    return LAW / f"{celex}.{LANG}.xhtml"


def fetch(celex: str, refresh: bool = False) -> Path:
    """Download the XHTML text of a CELEX number into the cache and return its path."""
    path = cache_path(celex)
    if path.exists() and not refresh:
        return path
    LAW.mkdir(parents=True, exist_ok=True)
    data = _request(CELLAR + celex, "application/xhtml+xml")
    if b"eli-subdivision" not in data and b"oj-" not in data:
        raise RuntimeError(f"{celex}: response does not look like a legal text ({len(data)} bytes)")
    path.write_bytes(data)
    return path


def load(celex: str, refresh: bool = False) -> ET.Element:
    return ET.parse(fetch(celex, refresh)).getroot()


def latest_consolidated(celex: str) -> list[str]:
    """CELEX numbers of the consolidated versions of a basic act (Cellar SPARQL)."""
    query = (
        "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> "
        "SELECT ?c WHERE { ?w cdm:resource_legal_id_celex "
        f'"{celex}"^^<http://www.w3.org/2001/XMLSchema#string> . '
        "?cons cdm:act_consolidated_based_on_resource_legal ?w . "
        "?cons cdm:resource_legal_id_celex ?c } ORDER BY ?c"
    )
    url = SPARQL + "?" + urllib.parse.urlencode({"query": query})
    rows = _request(url, "text/csv").decode("utf-8").splitlines()[1:]
    return [r.strip('"') for r in rows if r.strip()]


# ----------------------------------------------------------------- parsing
def _text(el: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def _divs(root: ET.Element):
    return root.iter(XH + "div")


def articles(root: ET.Element) -> dict[str, ET.Element]:
    return {d.get("id")[4:]: d for d in _divs(root)
            if re.fullmatch(r"art_[0-9]+[A-Za-z]?", d.get("id") or "")}


def recitals(root: ET.Element) -> dict[str, ET.Element]:
    return {d.get("id")[4:]: d for d in _divs(root) if re.fullmatch(r"rct_\d+", d.get("id") or "")}


def article_title(div: ET.Element) -> str:
    for d in div.iter(XH + "div"):
        if (d.get("id") or "").endswith(".tit_1"):
            return _text(d)
    return ""


def article_paragraphs(div: ET.Element) -> list[tuple[str, str]]:
    """(paragraph id, text) for the numbered paragraphs of an article."""
    out = []
    for d in div:
        if d.tag == XH + "div" and re.fullmatch(r"\d{3}\.\d{3}", d.get("id") or ""):
            out.append((d.get("id"), _text(d)))
    return out


def article_text(root: ET.Element, number: str, paragraph: str | None = None) -> str:
    arts = articles(root)
    if number not in arts:
        raise KeyError(f"article {number} not found (the text has {len(arts)} articles)")
    div = arts[number]
    head = f"Article {number}: {article_title(div)}"
    paras = article_paragraphs(div)
    if paragraph:
        paras = [(i, t) for i, t in paras if int(i.split(".")[1]) == int(paragraph)]
        if not paras:
            raise KeyError(f"article {number} has no paragraph {paragraph}")
    if not paras:  # articles without numbered paragraphs
        return head + "\n" + _text(div)
    return head + "\n" + "\n".join(t for _, t in paras)


# ---------------------------------------------------------------- manifest
def write_manifest(celexes: list[str]) -> None:
    items = {}
    for c in celexes:
        p = cache_path(c)
        items[c] = {
            "key": BY_CELEX.get(c, ""),
            "name": INSTRUMENTS[BY_CELEX[c]][1] if c in BY_CELEX else "",
            "language": LANG,
            "source": CELLAR + c,
            "retrieved": date.today().isoformat(),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "articles": len(articles(ET.parse(p).getroot())),
        }
    MANIFEST.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ------------------------------------------------------------------- check
ART_RE = re.compile(r"\bArticles?\s+((?:\d+[A-Za-z]?(?:\(\d+\))?(?:\s*(?:,|and|to|and/or)\s*)?)+)")


def _numbers(spec: str) -> list[str]:
    """Article numbers from '12, 14 and 26(1)' or '28 to 30'; ranges are expanded."""
    spec = re.sub(r"\(\d+\)", "", spec)
    parts = re.split(r"\s*(?:,|and/or|and)\s*", spec.strip())
    nums: list[str] = []
    for part in parts:
        m = re.fullmatch(r"(\d+)\s+to\s+(\d+)", part.strip())
        if m:
            nums += [str(n) for n in range(int(m.group(1)), int(m.group(2)) + 1)]
        elif part.strip():
            nums.append(re.sub(r"\s", "", part.strip()))
    return nums


def find_references(text: str) -> list[tuple[int, str, str]]:
    """(line number, instrument key, article number) for 'Article N ... <instrument>' in one sentence."""
    found = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.startswith("#") or "_references.md#source" in line and line.startswith("- "):
            continue
        for sentence in re.split(r"(?<=[.;:])\s+", line):
            keys = [k for k, (_, _, aliases) in INSTRUMENTS.items()
                    if any(re.search(rf"(?<![A-Za-z]){re.escape(a)}(?![A-Za-z])", sentence) for a in aliases)]
            if len(keys) != 1:  # none, or ambiguous: skip rather than guess
                continue
            for m in ART_RE.finditer(sentence):
                for n in _numbers(m.group(1)):
                    if re.fullmatch(r"\d+[A-Za-z]?", n):
                        found.append((lineno, keys[0], n))
    return found


def chapter_files() -> list[Path]:
    """Numbered manuscript files of the book (chapters, appendices), without the bibliography."""
    return sorted(p for p in DOCS.glob("[0-9][0-9]*_*.md") if not p.name.endswith("_references.md"))


def check(report: Path | None, files: list[Path] | None = None, strict: bool = False) -> int:
    """Check that cited articles exist in the instrument named in the same sentence.

    The match is heuristic: a sentence that names one instrument may cite an article of another
    (for example 'DORA ... Article 73 of the AI Act'). An article that is not found is therefore
    reported as NOT FOUND, to be read by hand, and fails the run only with ``strict``. A sentence
    that names the AI Act amendment (Regulation (EU) 2026/1744) is checked against the
    consolidated AI Act, which contains the amended articles.
    """
    files = files or chapter_files()
    roots: dict[str, dict[str, ET.Element]] = {}
    rows, notfound = [], 0
    for path in files:
        for lineno, key, n in find_references(path.read_text(encoding="utf-8")):
            target = "ai_act" if key == "ai_omnibus" else key
            if target not in roots:
                try:
                    roots[target] = articles(load(INSTRUMENTS[target][0]))
                except Exception as exc:  # network or parse failure
                    print(f"cannot load {target}: {exc}", file=sys.stderr)
                    roots[target] = {}
            div = roots[target].get(n)
            if div is None:
                notfound += 1
                rows.append((path.name, lineno, key, n, "NOT FOUND", "no such article in this instrument; the sentence may cite another"))
            else:
                rows.append((path.name, lineno, key, n, "ok", article_title(div)))
    lines = ["# Article references checked against Cellar", "",
             f"Checked {len(rows)} references in {len(files)} files on {date.today().isoformat()}; "
             f"{notfound} are not found in the instrument named in the same sentence (read these by hand). "
             "'ok' means the article exists, not that the sentence is right.", "",
             "| File | Line | Instrument | Article | Result | Title |", "|---|---|---|---|---|---|"]
    lines += [f"| {f} | {l} | {k} | {n} | {r} | {t} |" for f, l, k, n, r, t in rows]
    out = "\n".join(lines) + "\n"
    if report:
        report.write_text(out, encoding="utf-8")
    else:
        print(out)
    return 1 if (notfound and strict) else 0


# ------------------------------------------------------- Swedish statutes
SFS_URL = "https://data.riksdagen.se/dokument/sfs-{year}-{num}.text"
SFS: dict[str, tuple[str, str, list[str]]] = {
    "mbl": ("1976:580", "Lag (1976:580) om medbestämmande i arbetslivet (MBL)", ["MBL", "Lag (1976:580)", "Co-determination in the Workplace Act", "medbestämmandelagen"]),
    "forvaltningslag": ("2017:900", "Förvaltningslag (2017:900)", ["Förvaltningslag (2017:900)", "förvaltningslagen", "Administrative Procedure Act"]),
    "kommunallag": ("2017:725", "Kommunallag (2017:725)", ["Kommunallag (2017:725)", "kommunallagen", "Local Government Act"]),
    "tf": ("1949:105", "Tryckfrihetsförordning (1949:105)", ["Tryckfrihetsförordning (1949:105)", "tryckfrihetsförordningen", "Freedom of the Press Act"]),
    "arkivlag": ("1990:782", "Arkivlag (1990:782)", ["Arkivlag (1990:782)", "arkivlagen", "Archives Act"]),
    "osl": ("2009:400", "Offentlighets- och sekretesslag (2009:400)", ["Offentlighets- och sekretesslag (2009:400)", "offentlighets- och sekretesslagen", "Public Access to Information and Secrecy Act"]),
    "skadestandslag": ("1972:207", "Skadeståndslag (1972:207)", ["Skadeståndslag (1972:207)", "skadeståndslagen", "Tort Liability Act"]),
    "tillganglighetslag": ("2018:1937", "Lag (2018:1937) om tillgänglighet till digital offentlig service", ["Lag (2018:1937)", "Act on accessibility of digital public services"]),
    "cybersakerhetslag": ("2025:1506", "Cybersäkerhetslag (2025:1506)", ["Cybersäkerhetslag (2025:1506)", "cybersäkerhetslagen"]),
}
SFS_CHAPTER = re.compile(r"^(\d+ ?[a-z]?) kap\. [A-ZÅÄÖ]")
SFS_SECTION = re.compile(r"^(\d+ ?[a-z]?) §(?:\s|$)")


def sfs_path(nr: str) -> Path:
    return LAW / f"sfs-{nr.replace(':', '-')}.sv.txt"


def sfs_fetch(nr: str, refresh: bool = False) -> Path:
    path = sfs_path(nr)
    if path.exists() and not refresh:
        return path
    year, num = nr.split(":")
    LAW.mkdir(parents=True, exist_ok=True)
    data = _request(SFS_URL.format(year=year, num=num), "text/plain").decode("utf-8", "replace")
    if f"SFS nr:     {nr}" not in data:
        raise RuntimeError(f"SFS {nr}: response does not look like a statute")
    path.write_text(data, encoding="utf-8")
    return path


def sfs_sections(text: str) -> dict[tuple[str, str], str]:
    """{(chapter, section): text}; chapter is '' for statutes without chapters."""
    out: dict[tuple[str, str], str] = {}
    chapter, key, buf = "", None, []

    def flush() -> None:
        if key is not None:
            out[key] = re.sub(r"\s+", " ", " ".join(buf)).strip()

    prev_blank = True
    for line in text.splitlines():
        blank_before, prev_blank = prev_blank, not line.strip()
        if not blank_before:  # a heading or a section starts after a blank line; wrapped lines do not
            if key is not None:
                buf.append(line)
            continue
        m = SFS_CHAPTER.match(line)
        if m:
            flush(); key, buf = None, []
            chapter = m.group(1).replace(" ", "")
            continue
        m = SFS_SECTION.match(line)
        if m:
            flush()
            key, buf = (chapter, m.group(1).replace(" ", "")), [line]
            continue
        if key is not None:
            buf.append(line)
    flush()
    return out


def sfs_get(key: str, section: str, chapter: str | None) -> str:
    nr = SFS[key][0] if key in SFS else key
    secs = sfs_sections(sfs_fetch(nr).read_text(encoding="utf-8"))
    ck = (chapter or "").replace(" ", "")
    sk = section.replace(" ", "")
    if (ck, sk) not in secs:
        if not chapter:  # statute with chapters: list the matches
            hits = [f"{c} kap. {s} §" for (c, s) in secs if s == sk]
            raise KeyError(f"section {section} not found without chapter; found in: {', '.join(hits) or 'nowhere'}")
        raise KeyError(f"{chapter} kap. {section} § not found")
    return secs[(ck, sk)]


SFS_REF = re.compile(r"(?:(\d+\s?[a-z]?)\s+(?:kap\.|ch\.|Chapter)\s+)?(\d+\s?[a-z]?)\s*(?:§§?|sections?)", re.I)


def sfs_find_references(text: str) -> list[tuple[int, str, str, str]]:
    """(line, key, chapter, section) for section references in a sentence that names one Swedish statute."""
    found = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for sentence in re.split(r"(?<=[.;:])\s+", line):
            keys = [k for k, (_, _, al) in SFS.items() if any(re.search(re.escape(a), sentence) for a in al)]
            if len(keys) != 1:
                continue
            for m in SFS_REF.finditer(sentence):
                found.append((lineno, keys[0], (m.group(1) or "").replace(" ", ""), m.group(2).replace(" ", "")))
    return found


def sfs_check(report: Path | None) -> int:
    files = chapter_files()
    cache: dict[str, dict] = {}
    rows, problems = [], 0
    for path in files:
        for lineno, key, ch, sec in sfs_find_references(path.read_text(encoding="utf-8")):
            if key not in cache:
                try:
                    cache[key] = sfs_sections(sfs_fetch(SFS[key][0]).read_text(encoding="utf-8"))
                except Exception as exc:
                    print(f"cannot load {key}: {exc}", file=sys.stderr)
                    cache[key] = {}
            secs = cache[key]
            hit = secs.get((ch, sec)) or (None if ch else next((v for (c, s), v in secs.items() if s == sec), None))
            if hit is None:
                problems += 1
                rows.append((path.name, lineno, key, ch, sec, "MISSING", ""))
            else:
                rows.append((path.name, lineno, key, ch, sec, "ok", hit[:90]))
    lines = ["# Swedish statute references checked against the Riksdag's SFS text", "",
             f"Checked {len(rows)} references on {date.today().isoformat()}; {problems} point to a section that does not exist in the fetched text. "
             "'ok' means the section exists, not that the sentence is right.", "",
             "| File | Line | Statute | Chapter | Section | Result | Text begins |", "|---|---|---|---|---|---|---|"]
    lines += [f"| {f} | {l} | {k} | {c} | {s} | {r} | {t} |" for f, l, k, c, s, r, t in rows]
    out = "\n".join(lines) + "\n"
    if report:
        report.write_text(out, encoding="utf-8")
    else:
        print(out)
    return 1 if problems else 0


# --------------------------------------------------------------------- cli
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="the instruments the book uses")
    g = sub.add_parser("get", help="print an article, a recital or the table of articles")
    g.add_argument("instrument", help="key (see list) or a CELEX number, also consolidated such as 02024R1689-20260727")
    g.add_argument("--article")
    g.add_argument("--paragraph")
    g.add_argument("--recital")
    g.add_argument("--toc", action="store_true")
    g.add_argument("--refresh", action="store_true")
    lt = sub.add_parser("latest", help="consolidated versions of a basic act")
    lt.add_argument("celex")
    sub.add_parser("sync", help="download all instruments and write the manifest")
    c = sub.add_parser("check", help="check article references in docs/*.md")
    c.add_argument("--report", type=Path)
    c.add_argument("--strict", action="store_true", help="exit 1 if an article is not found")
    c.add_argument("files", nargs="*", type=Path)
    sf = sub.add_parser("sfs", help="Swedish statutes from the Riksdag's SFS database")
    sfsub = sf.add_subparsers(dest="sfs_cmd", required=True)
    sfsub.add_parser("list")
    sg = sfsub.add_parser("get")
    sg.add_argument("statute", help="key (see sfs list) or an SFS number such as 2017:900")
    sg.add_argument("--chapter")
    sg.add_argument("--section", required=True)
    sfsub.add_parser("sync")
    sc = sfsub.add_parser("check")
    sc.add_argument("--report", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "sfs":
        if a.sfs_cmd == "list":
            for k, (nr, name, _) in SFS.items():
                print(f"{k:20} {nr:10} {name}")
        elif a.sfs_cmd == "sync":
            bad = 0
            for k, (nr, name, _) in SFS.items():
                try:
                    sfs_fetch(nr, refresh=True)
                    print(f"ok   {nr} {name}")
                except Exception as exc:
                    bad += 1
                    print(f"FAIL {nr} {name}: {exc}", file=sys.stderr)
            return 1 if bad else 0
        elif a.sfs_cmd == "check":
            return sfs_check(a.report)
        else:
            print(sfs_get(a.statute, a.section, a.chapter))
        return 0
    if a.cmd == "list":
        for k, (celex, name, _) in INSTRUMENTS.items():
            print(f"{k:18} {celex:12} {name}")
        return 0
    if a.cmd == "latest":
        print("\n".join(latest_consolidated(a.celex)))
        return 0
    if a.cmd == "sync":
        done = []
        for k, (celex, name, _) in INSTRUMENTS.items():
            try:
                fetch(celex, refresh=True)
                done.append(celex)
                print(f"ok   {celex} {name}")
            except Exception as exc:
                print(f"FAIL {celex} {name}: {exc}", file=sys.stderr)
        write_manifest(done)
        return 0 if len(done) == len(INSTRUMENTS) else 1
    if a.cmd == "check":
        return check(a.report, a.files or None, a.strict)
    root = load(resolve(a.instrument), a.refresh)
    if a.toc:
        for n, d in articles(root).items():
            print(f"Article {n}: {article_title(d)}")
    elif a.recital:
        print(_text(recitals(root)[a.recital]))
    elif a.article:
        print(article_text(root, a.article, a.paragraph))
    else:
        ap.error("give --article, --recital or --toc")
    return 0


if __name__ == "__main__":
    sys.exit(main())
