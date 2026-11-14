"""Offline tests of the Cellar text parser (no network)."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fetch_eu_law as f  # noqa: E402

SAMPLE = """<html xmlns="http://www.w3.org/1999/xhtml"><body>
<div class="eli-subdivision" id="art_35"><p class="oj-ti-art">Article 35</p>
<div class="eli-title" id="art_35.tit_1"><p>Data protection impact assessment</p></div>
<div id="035.001"><p>1. Where a type of processing is likely to result in a high risk.</p></div>
<div id="035.002"><p>2. The controller shall seek the advice of the data protection officer.</p></div></div>
<div class="eli-subdivision" id="art_36"><p>Article 36</p><div class="eli-title" id="art_36.tit_1"><p>Prior consultation</p></div></div>
</body></html>"""


def test_articles_and_paragraphs() -> None:
    root = ET.fromstring(SAMPLE)
    assert list(f.articles(root)) == ["35", "36"]
    assert f.article_title(f.articles(root)["35"]) == "Data protection impact assessment"
    text = f.article_text(root, "35", "2")
    assert "data protection officer" in text and "high risk" not in text


def test_reference_extraction() -> None:
    text = "The controller carries out an assessment under GDPR Articles 25, 32 and 35(1) and Article 9 of the GDPR."
    refs = {(k, n) for _, k, n in f.find_references(text)}
    assert refs == {("gdpr", "25"), ("gdpr", "32"), ("gdpr", "35"), ("gdpr", "9")}


def test_ranges_are_expanded() -> None:
    assert f._numbers("28 to 30") == ["28", "29", "30"]


SFS_SAMPLE = """Testlag (2000:1)

1 kap. Inledning

Rubrik

1 § Första paragrafen börjar här
och fortsätter på en andra rad.

2 § Andra paragrafen. Den hänvisar till
1 kap. 1 § men det är en radbruten rad.

2 kap. Fortsättning

1 § En annan första paragraf.
"""


def test_sfs_sections_handle_chapters_and_wrapped_lines() -> None:
    secs = f.sfs_sections(SFS_SAMPLE)
    assert set(secs) == {("1", "1"), ("1", "2"), ("2", "1")}
    assert "radbruten" in secs[("1", "2")]
    assert secs[("2", "1")].startswith("1 § En annan")
