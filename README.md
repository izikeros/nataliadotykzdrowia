# Nowa strona Dotyk Zdrowia (wersja zaakceptowana przez Natalię, 9.11.2026)

Gotowe, statyczne strony HTML, zaakceptowane przez Natalię. Podgląd:
https://dotyk-zdrowia-podglad.vercel.app (podgląd ma `noindex`, w tej paczce go nie ma).

## Strony

| Plik                             | Adres                  | Odpowiednik na obecnej stronie |
| -------------------------------- | ---------------------- | ------------------------------ |
| `index.html`                     | `/`                    | strona główna                  |
| `o-mnie/index.html`              | `/o-mnie/`             | `/o-mnie/`                     |
| `opinie/index.html`              | `/opinie/`             | `/opinie/`                     |
| `analiza-zdrowia/index.html`     | `/analiza-zdrowia/`    | nowa                           |
| `droga-do-rownowagi/index.html`  | `/droga-do-rownowagi/` | nowa                           |
| `wspolpraca-online/index.html`   | `/wspolpraca-online/`  | nowa (zastępuje sekcję online z `/oferta/`) |
| `kurs-online/index.html`         | `/kurs-online/`        | nowa                           |
| `analiza-zdrowia-mezczyzni/index.html`    | `/analiza-zdrowia-mezczyzni/`    | nowa (wersja dla mężczyzn) |
| `droga-do-rownowagi-mezczyzni/index.html` | `/droga-do-rownowagi-mezczyzni/` | nowa (wersja dla mężczyzn) |

`/oferta/` nie ma odpowiednika. Warto ustawić przekierowanie 301 z `/oferta/` na `/`
albo na `/droga-do-rownowagi/`.

## Zasoby

- `assets/landing-c.css` i `assets/wspolne.css` to style podstron. Strona główna ma style
  w samym pliku.
- `assets/img/` to zdjęcia (webp/avif).
- Wszystkie ścieżki są od korzenia (`/assets/...`, `/o-mnie/`). Nazwy nie kolidują
  z obecnymi `assets/css`, `assets/js` i `assets/images`.
- Czcionki są z Google Fonts. Dwie grafiki ładują się z `cdn.idealms.net`: zdjęcie
  na stronie współpracy online i grafika materiałów w kursie.

## Linki zewnętrzne (bez zmian)

- Rezerwacje: https://dotykzdrowia.simplybook.it/v2/book/
- Zakupy: `sklep.nataliadotykzdrowia.pl` (proces, współpraca online, kurs)
- Newsletter / analiza stóp: https://dotyk-zdrowia-natalia-safjan-analiza.subscribepage.io/
- Opinie Google: https://share.google/dkdeNXWsFwR2Cn5j5

Stopka prowadzi do `/polityka-prywatnosci/` i `/regulamin-newslettera/`. To obecne
strony z `build.py`, więc powinny zostać.

## Strony dla mężczyzn (dodane 17.11.2026)

- `analiza-zdrowia-mezczyzni/` i `droga-do-rownowagi-mezczyzni/` używają tych samych
  stylów co pozostałe podstrony. Nowe zdjęcie: `assets/img/zabieg-mezczyzna.avif`.
- Strony męskie linkują do siebie nawzajem. Z menu i strony głównej nie prowadzi do nich
  żaden link, więc trzeba je dopisać do tras (`PAGES` w `build.py`, `ROUTES` w `check.py`)
  i ewentualnie do sitemapy.

## Czego tu nie ma

- Zmian w `build.py`, `docs/` i `dist/`. Ta paczka niczego nie podmienia. Decyzja,
  jak włączyć strony (zastąpić wynik `build.py` czy przenieść treść do generatora),
  należy do Ciebie.
