# Genomgång av PR #262 och Uppdatering av GitHub Issues

## Sammanfattning

Detta dokument sammanfattar genomgången av [PR #262](https://github.com/Geonitab/architecture_as_code/pull/262) och identifierar vilka GitHub issues som behöver uppdateras baserat på de sammanslagningar som gjorts.

## Vad PR #262 Innehåller

PR #262 lade till "Linked Pull Requests"-sektioner till 11 issue-mallfiler i `issues/`-katalogen. Detta dokumenterar kopplingen mellan:
- Issue-mallar (beskriver arbete som ska göras)
- Pull requests (genomförande av arbetet)
- GitHub issues (spårning av arbetet)

## Issue-Mallfiler som Uppdaterades

| Issue-mall | Länkade PRs |
|-----------|-------------|
| `006-remove-chapter-6.md` | [#254](https://github.com/Geonitab/architecture_as_code/pull/254) - Ta bort Kapitel 6 |
| `007-refresh-chapter-7.md` | [#256](https://github.com/Geonitab/architecture_as_code/pull/256) - Uppdatera Kapitel 7 till brittisk engelska |
| `009-translate-chapter-9.md` | [#247](https://github.com/Geonitab/architecture_as_code/pull/247) och [#258](https://github.com/Geonitab/architecture_as_code/pull/258) - Översätt Kapitel 9 |
| `012-complete-chapter-12-diagrams.md` | [#248](https://github.com/Geonitab/architecture_as_code/pull/248) - Lägg till diagram för Kapitel 12 |
| `014-update-chapter-14.md` | [#253](https://github.com/Geonitab/architecture_as_code/pull/253) - Revidera Kapitel 14 |
| `018-balance-chapter-18.md` | [#259](https://github.com/Geonitab/architecture_as_code/pull/259) - Ta bort PNG-filer från Kapitel 18 |
| `020-rewrite-chapter-20.md` | [#251](https://github.com/Geonitab/architecture_as_code/pull/251) - Omskriv Kapitel 20 |
| `025-026-merge-chapters.md` | [#249](https://github.com/Geonitab/architecture_as_code/pull/249) - Slå samman Kapitel 25 och 26 |
| `027-refresh-chapter-27.md` | [#250](https://github.com/Geonitab/architecture_as_code/pull/250) - Uppdatera Kapitel 27 |
| `028-expand-chapter-28-glossary.md` | [#257](https://github.com/Geonitab/architecture_as_code/pull/257) - Utöka ordlistan i Kapitel 28 |
| `031-update-chapter-31.md` | [#252](https://github.com/Geonitab/architecture_as_code/pull/252) - Översätt och förtydliga Kapitel 31 |

## Öppna Issues som Behöver Uppdateras

Följande GitHub issues är fortfarande öppna och bör uppdateras med information om deras länkade PRs:

1. **Issue #220** - "Refresh Chapter 7" → PR #256
2. **Issue #222** - "Update Chapter 31" → PR #252
3. **Issue #227** - "Translate Chapter 9" → PR #247, #258
4. **Issue #228** - "Rewrite Chapter 20" → PR #251
5. **Issue #229** - "Expand Chapter 28 Glossary" → PR #257
6. **Issue #230** - "Refresh Chapter 27" → PR #250
7. **Issue #231** - "Update Chapter 14" → PR #253
8. **Issue #232** - "Balance Chapter 18" → PR #259
9. **Issue #237** - "Complete Chapter 12 Diagrams" → PR #248

## Rekommenderade Åtgärder

### För varje öppet issue:

1. **Lägg till en kommentar** som dokumenterar den länkade PR:en
2. **Granska PR:en** för att verifiera om alla uppgifter och acceptanskriterier är uppfyllda
3. **Stäng issuen** om allt är färdigt, eller uppdatera uppgiftslistan om arbete kvarstår

### Detaljerade uppdateringsinstruktioner

Se dokumentet `ISSUE_UPDATES_FROM_PR262.md` för exakt text som ska läggas till i varje issue.

### Automatisering med GitHub CLI

Du kan använda GitHub CLI för att uppdatera issues automatiskt:

```bash
# Exempel för issue #220
gh issue comment 220 --body "## Linked Pull Request

This issue has been addressed by:
- [#256 Refresh Chapter 7 for British English consistency](https://github.com/Geonitab/architecture_as_code/pull/256) — merged on 2025-10-12 at 18:38 UTC

Please review the PR to verify all tasks and acceptance criteria have been met."
```

## Redan Stängda Issues

Följande issues var redan stängda när denna genomgång gjordes:

- **Issue #234** - "Retire Chapter 6" → PR #254
- **Issue #235** - "Merge Chapters 25 And 26" → PR #249
- **Issue #236** - "Retire Chapter 8" → Stängd (ingen PR-länk hittades i mallar)
- **Issue #238** - "Retire Chapter 22" → Stängd (ingen PR-länk hittades i mallar)

## Resultat av Genomgången

PR #262 har framgångsrikt dokumenterat kopplingen mellan issue-mallar och deras motsvarande pull requests. Detta ger spårbarhet och gör det lättare att följa arbetsflödet från issue till genomförande.

### Nästa Steg

1. Uppdatera de 9 öppna issues med PR-information
2. Granska varje PR för att bekräfta fullständighet
3. Stäng issues där allt arbete är färdigt
4. Överväg att implementera automatisering för framtida synkronisering mellan issue-mallar och GitHub issues

## Relaterade Dokument

- `PR_262_REVIEW_SUMMARY.md` - Detaljerad genomgång på engelska
- `ISSUE_UPDATES_FROM_PR262.md` - Exakta uppdateringstexter för varje issue
