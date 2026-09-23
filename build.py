#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the database-free Dotyk Zdrowia static site."""

from pathlib import Path
from shutil import copy2, rmtree
from html import escape
import argparse
import re

ROOT = Path(__file__).parent
OUT = ROOT / "dist"
MISC = ROOT.parent / "misc"
UPLOADS = ROOT.parent / "wp-content" / "uploads"

NAV = (
    ('/o-mnie/', 'O mnie'),
    ('/oferta/#terapia-holistyczna', 'Współpraca 1:1'),
    ('https://sklep.nataliadotykzdrowia.pl', 'Kursy Online'),
    ('/opinie/', 'Opinie'),
    ('https://dotykzdrowia.simplybook.it/v2/#book', 'Umów Wizytę'),
    ('/#kontakt', 'Kontakt'),
)

TESTIMONIAL_IMAGES = (
    "1_ewa.png", "2_agata.png", "IMG_3641.jpg", "IMG_3634.jpg", "21.png", "24.png",
    "22.png", "27.png", "3.png", "2.jpg", "14.png", "8.png", "12.png", "19.png",
    "5.png", "15.png", "1.png", "6.png", "4.png", "7.png", "9.png", "10.png",
    "11.png", "13.png", "16.png", "17.png", "18a.png", "20.png", "25.png",
    "26.png", "28.png", "29.png",
)

HOME_TESTIMONIAL_IMAGES = (
    "1_ewa.png",
    "IMG_3634.jpg",
    "IMG_3641.jpg",
    "14.png",
    "12.png",
    "22.png",
    "24.png",
)


def testimonial_gallery(images, class_name="review-grid"):
    return f'<div class="{class_name}">' + "".join(
        f'<img src="/assets/images/{name}" alt="Opinia klientki" loading="lazy">'
        for name in images
    ) + "</div>"


def testimonial_rows(rows, class_name):
    return f'<div class="{class_name} testimonial-rows">' + "".join(
        f'<div class="testimonial-row testimonial-row-{len(row)}">'
        + "".join(
            f'<img src="/assets/images/{name}" alt="Opinia klientki" loading="lazy">'
            for name in row
        )
        + "</div>"
        for row in rows
    ) + "</div>"


def shared(title, description, content, path):
    links = "".join(
        '<a href="{}"{}>{}</a>'.format(
            href,
            ' aria-current="page"' if path == href else "",
            label,
        )
        for href, label in NAV
    )
    return f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description)}">
  <title>{escape(title)} | Dotyk Zdrowia Natalia Safjan</title>
  <link rel="canonical" href="https://nataliadotykzdrowia.pl{path}">
  <link rel="icon" href="/assets/images/cropped-fav-32x32.png" sizes="32x32">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/fontawesome.min.css">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#content">Przejdź do treści</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="/" aria-label="Dotyk Zdrowia - strona główna">
        <img src="/assets/images/logo.png" width="300" height="69" alt="Dotyk Zdrowia">
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" class="site-nav" aria-label="Główna nawigacja">{links}</nav>
    </div>
  </header>
  <main id="content">{content}</main>
  <footer class="site-footer">
    <div class="container footer-bottom">
      <p>Copyright 2026 Natalia Safjan<br><a href="/polityka-prywatnosci/">Polityka prywatności</a></p>
    </div>
  </footer>
  <a class="scroll-top" href="#" data-scroll-top hidden aria-label="Przewiń do początku strony"><i class="fas fa-angle-up" aria-hidden="true"></i></a>
  <section class="consent" data-consent hidden aria-label="Ustawienia cookies">
    <div><h2>Twoja prywatność</h2><p>Używamy niezbędnego zapisu wyboru cookies. Za zgodą możemy uruchomić formularz newslettera MailerLite.</p></div>
    <div class="consent-actions"><button type="button" data-consent-choice="essential">Tylko niezbędne</button><button type="button" data-consent-choice="all">Akceptuję</button></div>
  </section>
  <dialog class="newsletter-dialog" data-newsletter aria-labelledby="newsletter-title">
    <button class="dialog-close" type="button" data-close-newsletter aria-label="Zamknij">×</button>
    <h2 id="newsletter-title">Bądź bliżej swojego zdrowia</h2>
    <p>Zapisz się do newslettera, aby otrzymywać wskazówki i informacje od Natalii.</p>
    <div data-mailerlite-form><a class="button" href="/regulamin-newslettera/">Przeczytaj regulamin newslettera</a></div>
  </dialog>
</body>
</html>"""


HOME = f"""
<section class="hero hero-home"><div class="container hero-frame split">
  <div class="hero-image"><img src="/assets/images/profilowe-zdjece.jpg" width="486" height="486" alt="Natalia Safjan"></div>
  <div class="hero-copy"><p class="eyebrow">Holistyczne terapie naturalne dla kobiet 35+</p><h1>Czujesz, że Twój organizm od dłuższego czasu wysyła Ci sygnały?</h1>
  <p>Bóle i napięcia, zmęczenie, problemy ze snem, trawieniem czy gospodarką hormonalną… <strong>Masz kilka różnych dolegliwości, ale nie wiesz, czy coś je ze sobą łączy ani od czego właściwie zacząć?</strong></p>
  <p>Jestem Natalia Safjan, Terapeutka Holistyczna, Dyplomowany Refleksolog i Terapeutka baniek z ponad 10-letnim doświadczeniem.</p>
  <p><strong>Sama byłam kiedyś w miejscu, w którym być może jesteś dziś.</strong> Wiem, jak wyczerpujące może być życie z różnymi dolegliwościami. Ale wiem też, jak wiele może dać „połączenie kropek”, lepsze zrozumienie swojego organizmu i znalezienie własnego sposobu dbania o zdrowie.</p>
  <p>Pomagam kobietom, które nie chcą już zajmować się swoim zdrowiem fragmentarycznie. Patrzę na organizm <strong>całościowo</strong>, <strong>szukając zależności</strong> między tym, co dzieje się w różnych jego obszarach, a następnie <strong>indywidualnie dobieram i łączę metody pracy.</strong></p>
  <p><strong>Nie musisz wybierać jednego zabiegu do jednego problemu.</strong></p>
  <p><strong>Podczas jednej sesji możemy połączyć kilka uzupełniających się synergicznie metod</strong>, dzięki czemu nie musisz tracić czasu na odwiedzanie różnych miejsc i korzystanie z każdej metody osobno.</p>
  <p>Zależy mi, żeby sposób pracy był <strong>dopasowany do Ciebie, Twoich potrzeb i Twojego życia</strong>, a nie oparty na gotowym schemacie.</p>
  <p>Bo <strong>Twój czas jest cenny</strong>. Dbanie o zdrowie nie powinno oznaczać kolejnych godzin spędzonych na szukaniu różnych rozwiązań i odwiedzaniu kolejnych miejsc. Ma pomóc Ci odzyskać więcej energii i przestrzeni na to, co jest dla Ciebie naprawdę ważne.</p>
  <p>Możemy pracować ze sobą <strong>w gabinecie we Wrocławiu, online 1:1 lub poprzez moje kursy online.</strong></p>
  <p>Więcej o mnie przeczytasz <a href="/o-mnie/"><strong>tutaj</strong></a>.</p>
  <a class="button button-icon" href="https://dotykzdrowia.simplybook.it/v2/#book" target="_blank" rel="noopener"><i class="far fa-calendar-alt" aria-hidden="true"></i><span>Sprawdź dostępność wizyt</span></a></div>
</div></section>
<section class="section home-offer"><div class="container"><h2 class="section-heading">Oferta</h2><div class="cards">
  <article><img src="/assets/images/refl-twarzy.jpg" width="626" height="417" alt="Terapia refleksologiczna"><h3><a href="/oferta/#terapia-holistyczna">Holistyczna terapia naturalna w gabinecie we Wrocławiu</a></h3><p>Współpracę rozpoczynamy od <strong>Holistycznej analizy Twojego zdrowia</strong> – zatrzymujemy się, by spojrzeć na Twój organizm jako całość i <strong>połączyć kropki między różnymi dolegliwościami, Twoją historią i codziennością</strong>.</p><p>Na tej podstawie określam <strong>indywidualny kierunek pracy i dobieram odpowiednie dla Ciebie metody</strong>. W zależności od Twoich aktualnych potrzeb łączę m.in. refleksologię, terapię próżniową, aromaterapię i terapię ciepłem.</p><p>Pracuję procesowo, indywidualnie dopasowując metody do Ciebie w ramach Twojej <strong>Holistycznej drogi do równowagi</strong>.</p><p>Szczegóły znajdziesz w <a href="/oferta/#terapia-holistyczna"><strong>opisie usługi</strong></a>.</p></article>
  <article><img src="/assets/images/zjecie_konsultacja-online.webp" width="1536" height="1024" alt="Konsultacja online"><h3><a href="/oferta/#online">Holistyczna współpraca indywidualna online</a></h3><p>Proces online, w którym zatrzymujemy się i przyglądamy Twojemu organizmowi całościowo, analizując Twoje dolegliwości i styl życia, by znaleźć metody, które najpełniej Cię wesprą.</p><p>Na tej podstawie otrzymujesz <strong>indywidualne zalecenia oraz instruktaże wideo z metodami autoterapii refleksologicznej i/lub akupresurowej</strong>, dopasowanymi do Ciebie, Twoich potrzeb i zgłaszanych dolegliwości.</p><p>Dzięki temu możesz <strong>samodzielnie pracować ze swoim ciałem we własnym tempie</strong>, korzystając z przygotowanych dla Ciebie materiałów wtedy, kiedy ich potrzebujesz.</p><p>To proces, który nie tylko pomaga poczuć się lepiej, ale daje Ci narzędzia do budowania równowagi i dbania o zdrowie na co dzień.</p><p>Szczegóły znajdziesz w <a href="/oferta/#online"><strong>opisie usługi</strong></a>.</p></article>
</div></div></section>
<section class="section home-reviews"><div class="container narrow"><h2 class="section-heading">Opinie moich Klientów</h2><p>Każda opinia, którą zostawiacie po wizycie, jest dla mnie ogromnym darem — potwierdzeniem, że to, co robię, ma sens.</p><p>Poniżej znajdziesz wybrane opinie osób, które skorzystały z moich terapii. To słowa pochodzące z recenzji na Facebooku oraz w wizytówce Google.</p></div>{testimonial_rows((HOME_TESTIMONIAL_IMAGES[:3], HOME_TESTIMONIAL_IMAGES[3:]), "home-review-grid")}<div class="review-actions"><a class="button button-icon" href="/opinie/"><i class="far fa-comment" aria-hidden="true"></i><span>Zobacz więcej opinii</span></a><a class="button button-icon" href="https://dotykzdrowia.simplybook.it/v2/#book" target="_blank" rel="noopener"><i class="far fa-calendar-alt" aria-hidden="true"></i><span>Umów wizytę</span></a></div></section>
<section id="kontakt" class="section contact-section"><div class="container contact-panel"><h2 class="section-heading">Kontakt</h2><div class="contact-grid"><div class="contact-logo"><img src="/assets/images/logo.png" width="748" height="172" alt="Dotyk Zdrowia"></div><div class="contact-details"><a class="contact-item" href="tel:739906575"><span class="contact-icon"><i class="fas fa-phone" aria-hidden="true"></i></span><span>739 90 65 75</span></a><a class="contact-item" href="https://www.facebook.com/nataliadotykzdrowia" target="_blank" rel="noopener"><span class="contact-icon"><i class="fab fa-facebook-f" aria-hidden="true"></i></span><span>@nataliadotykzdrowia</span></a><a class="contact-item" href="https://www.instagram.com/nataliadotykzdrowia/" target="_blank" rel="noopener"><span class="contact-icon"><i class="fab fa-instagram" aria-hidden="true"></i></span><span>@nataliadotykzdrowia</span></a><a class="button button-icon" href="https://dotykzdrowia.simplybook.it/v2/#book" target="_blank" rel="noopener"><i class="far fa-calendar-alt" aria-hidden="true"></i><span>Umów wizytę</span></a></div></div></div></section>
"""

ABOUT = """
<section class="about-hero"><div class="container about-frame split"><div class="about-image"><h1>O mnie</h1><img src="/assets/images/natalia.jpg" width="487" height="487" alt="Natalia Safjan"></div>
<div class="about-copy"><p>Pasja do medycyny naturalnej i holistycznego podejścia do zdrowia towarzyszy mi od ponad 10 lat.</p><p>Zaczęła się – jak to często bywa – od osobistych doświadczeń. Pracując intensywnie w korporacji, z czasem zaczęłam odczuwać skutki życia w ciągłym biegu. Zdrowie i odpoczynek odkładałam na później, sięgając po szybkie rozwiązania i kolejne tabletki. Dopiero problemy zdrowotne moje i moich bliskich sprawiły, że zaczęłam szukać prawdziwych przyczyn i trwałych rozwiązań.</p><p>Właśnie wtedy odkryłam moc medycyny naturalnej. Szczególne miejsce zajęły w niej refleksologia – technika stymulacji punktów na stopach i dłoniach odpowiadających za pracę narządów – oraz terapia bańkami, która pomogła mi wyjść z zaawansowanego zapalenia płuc.</p><p>Z czasem ta pasja zaczęła zajmować coraz więcej miejsca w moim życiu. A ponieważ zawsze stawiam na rzetelność i jakość, przyszły kolejne szkolenia, książki i setki godzin praktyki. Tak rozpoczęła się moja nowa, zawodowa droga.</p><p>Ukończyłam wszystkie stopnie nauki refleksologii, zdałam egzaminy teoretyczne i praktyczne uzyskując tytuł zawodowy Dyplomowanego refleksologa stóp, dłoni, twarzy i głowy. Jestem także certyfikowanym terapeutą baniek lekarskich, chińskich i sportowych. Dziś z pełnym przekonaniem mogę powiedzieć, że robię to, co kocham – wspieram innych w odzyskiwaniu zdrowia, równowagi i spokoju.</p><p>Efekty pracy z moimi klientami są niezwykle satysfakcjonujące – zarówno dla nich, jak i dla mnie. Wśród licznych pozytywnych zmian, jakie obserwuję, są m.in. zmniejszenie objawów astmy oskrzelowej, redukcja bólów kręgosłupa, wyciszenie układu nerwowego przy przewlekłym stresie, zmniejszenie natężenia migren czy poprawa samopoczucia przy stanach depresyjnych.</p><p>Jeśli chcesz zobaczyć, jak wygląda moja praca na co dzień i jak terapie holistyczne mogą wspierać Twoje zdrowie – serdecznie zapraszam do kontaktu i umówienia się na zabieg.</p><a class="button" href="https://dotykzdrowia.simplybook.it/v2/#book" target="_blank" rel="noopener">Umów wizytę</a></div></div></section>
"""

OFFER = """
<section class="offer-intro"><div class="container"><div class="offer-intro-image"><img src="/assets/images/refl-twarzy.jpg" width="626" height="417" alt="Holistyczna terapia naturalna"></div><div class="offer-intro-title"><h1>Holistyczna terapia naturalna we Wrocławiu</h1></div></div></section>
<section id="terapia-holistyczna" class="offer-section offer-content"><div class="container"><h2>Etap 1: Holistyczna analiza Twojego zdrowia i pierwsza indywidualnie dobrana terapia</h2><p>To <strong>pierwszy krok w Twoim indywidualnym, szytym na miarę procesie</strong>, który pozwoli Ci się na chwilę zatrzymać, przyjrzeć się swojemu organizmowi i zrobić coś dla siebie.</p><p><strong>By wiedzieć jak dotrzeć tam gdzie chcemy, potrzebujemy najpierw zrozumieć gdzie jesteśmy.</strong></p><p>Taki jest właśnie cel naszego pierwszego spotkania, czyli Holistycznej analizy Twojego zdrowia. Ma ona na celu poznanie Twojej sytuacji zdrowotnej i życiowej, dopasowanie właściwych dla Ciebie metod i uzyskanie pierwszych wskazówek. Przeprowadzę również <strong>pierwszą celowaną w Twoje problemy terapię holistyczną</strong>, byś mogła być już o ten „krok bliżej swojego zdrowia”.</p><h3>Jak będzie przebiegać nasza współpraca?</h3><p>Jeszcze zanim się spotkamy wypełniasz <strong>kwestionariusz zdrowotny</strong>, który dokładnie analizuję przed wizytą. Zwracam uwagę na Twoją historię i zgłaszane dolegliwości, ich wzajemne powiązanie, a także wykres urodzeniowy BaZi.</p><p>Podczas spotkania łączę te informacje z rozmową, badaniem refleksologicznym obszarów na stopach i analizą, które z meridianów mogą być u Ciebie zablokowane. Na tej podstawie <strong>określam kierunek dalszej pracy</strong> i już podczas pierwszego spotkania rozpoczynamy indywidualnie dobraną terapię.</p><p>Podczas sesji dobieram najskuteczniejsze techniki lub łączę kilka metod, by uzyskać <strong>maksymalny efekt terapeutyczny i głęboki relaks</strong>.</p><p><strong>W pracy wykorzystuję między innymi:</strong></p><ul><li>refleksologię stóp, dłoni, twarzy i głowy,</li><li>terapię próżniową bańkami,</li><li>aromaterapię,</li><li>terapię ciepłem lampy TDP.</li></ul><p>Zwykle korzystam z kilku metod w czasie jednego spotkania, by efektywnie wykorzystać ich potencjał synergiczny i zaoszczędzić Twój czas.</p><h3>Inwestycja w analizę:</h3><p><strong>320 zł (sesja trwa około 75 min)</strong></p><p>Jeśli zdecydujesz się na dalszą pracę ze mną w ramach procesu Holistycznej drogi do zdrowia, koszt pierwszego spotkania zostanie odjęty od ceny procesu.</p><h3>Co się dzieje po spotkaniu?</h3><p>Po spotkaniu dostajesz <strong>spersonalizowane zalecenia</strong> oraz informacje, jakie formy wsparcia byłyby dla Ciebie korzystne. Dowiesz się również, czy dalsze etapy współpracy w ramach <a href="https://sklep.nataliadotykzdrowia.pl/product/holistyczna-naturalna-droga-do-rownowagi/" target="_blank" rel="noopener">Holistycznej naturalnej drogi do równowagi</a> będą w Twoim przypadku zasadne.</p><div class="offer-cta"><a class="button" href="https://dotykzdrowia.simplybook.it/v2/#book/location/1/service/3/count/1/" target="_blank" rel="noopener">Tak, to coś dla mnie! Umawiam się na moją Holistyczną analizę zdrowia</a></div></div></section>
<section class="offer-section offer-content offer-continuation"><div class="container"><p>Jeśli okaże się, że <strong>dalszy proces nie jest Ci potrzebny, również Ci o tym powiem</strong>. Jeżeli uznam, że w Twoim przypadku bardziej odpowiednia będzie praca z innym specjalistą, również Ci to zasugeruję.</p><p>Zależy mi przede wszystkim na tym, abyś otrzymała <strong>wsparcie dopasowane do Ciebie, Twoich potrzeb i aktualnej sytuacji</strong> – niezależnie od tego, czy będzie to dalsza współpraca ze mną, czy inna forma wsparcia.</p><h2>Etap 2: Holistyczna naturalna droga do równowagi</h2><p>Jeśli poczujesz, że chcesz zrobić kolejny krok, <strong>Holistyczna naturalna droga do równowagi</strong> jest naturalną kontynuacją naszej współpracy – indywidualnym procesem, który tworzę i dopasowuję do Ciebie na kolejnych etapach.</p><div class="offer-cta"><a class="button" href="https://sklep.nataliadotykzdrowia.pl/product/holistyczna-naturalna-droga-do-rownowagi/" target="_blank" rel="noopener">Chcę przeczytać więcej o procesie Holistycznej naturalnej drogi do równowagi</a></div><div id="online" class="offer-online"><img src="/assets/images/zjecie_konsultacja-online.webp" width="1536" height="1024" alt="Indywidualna współpraca online"><h2>Holistyczna terapia współpraca indywidualna ONLINE</h2><h3>W trakcie naszej współpracy nauczysz się samodzielnie regulować napięcie w ciele, zmniejszać ból i wspierać organizm w regeneracji dzięki refleksologii i akupresurze.</h3><p>W ciągu kilku tygodni poznasz dopasowany do Ciebie i Twoich dolegliwości prosty system autoterapii, który pozwoli Ci:</p><ul><li>reagować na pierwsze sygnały bólu i napięcia,</li><li>poprawić sen i poziom energii,</li><li>zmniejszać stres i napięcia emocjonalne,</li><li>wprowadzić krótkie codzienne rytuały wspierające zdrowie,</li><li>odzyskać poczucie wpływu na swoje ciało.</li></ul><p>I wreszcie czuć się lepiej. Nie dlatego, że ktoś Cię „naprawił”, tylko dlatego, że nauczyłaś się pracować ze swoim ciałem.</p><h3>Korzyści z holistycznej pracy 1:1</h3><p>Praca w oparciu o refleksologię i akupresurę pozwala zrozumieć sygnały własnego ciała, skutecznie wspierać zdrowie w domu, redukować napięcia oraz zyskać niezależność w samodzielnym stosowaniu technik.</p><p><strong>💡 Dla kogo jest współpraca holistyczna?</strong></p><ul><li>Dla osób, które chcą wziąć zdrowie w swoje ręce.</li><li>Dla osób gotowych do samodzielnej pracy w domu.</li><li>Dla tych, którzy chcą zrozumieć swoje ciało i nauczyć się reagować na jego sygnały.</li></ul><p><strong>💡 Dla kogo to nie jest?</strong></p><ul><li>Dla osób oczekujących, że ktoś zrobi wszystko za nie.</li><li>Dla osób bez czasu na regularną praktykę.</li><li>Dla osób szukających szybkich, natychmiastowych efektów.</li></ul><p>To nie jest jednorazowe rozwiązanie ani „magiczna metoda”. Pracujemy procesowo – stopniowo regulując organizm i docierając do przyczyn.</p><p>Wprowadziłam możliwość współpracy w <strong>2 wersjach – 6–8 tygodniowej (STANDARD) oraz 8–12 tygodniowej (PREMIUM)</strong>.</p><p>Szczegóły znajdziesz po kliknięciu w przyciski poniżej:</p></div><div class="offer-packages"><a class="button" href="https://sklep.nataliadotykzdrowia.pl/product/online-indywidualna-wspolpraca-holistyczna-wersja-standard/" target="_blank" rel="noopener">Wersja STANDARD</a><a class="button" href="https://sklep.nataliadotykzdrowia.pl/product/indywidualna-wspolpraca-holistyczna-online/" target="_blank" rel="noopener">Wersja PREMIUM</a></div></div></section>
"""

REVIEWS = """
<section class="reviews-intro"><div class="container"><h1>Poniżej znajdziesz więcej opinii osób, którym towarzyszyłam w ich drodze do zdrowia. To słowa, które pojawiły się w recenzjach na Facebooku i w wizytówce Google.</h1></div></section>
<section class="reviews-gallery">""" + testimonial_rows(
    (
        TESTIMONIAL_IMAGES[:3],
        TESTIMONIAL_IMAGES[3:8],
        *tuple(
            TESTIMONIAL_IMAGES[index:index + 2]
            for index in range(8, len(TESTIMONIAL_IMAGES), 2)
        ),
    ),
    "review-grid",
) + """</section>
<section class="reviews-cta"><div class="container"><p>Jeśli chcesz, bym i Ciebie wsparła w Twojej drodze do dobrego zdrowia poniżej znajdziesz link do zapisów:</p><a class="button button-icon" href="https://dotykzdrowia.simplybook.it/v2/#book" target="_blank" rel="noopener"><i class="far fa-calendar-alt" aria-hidden="true"></i><span>Umów wizytę</span></a></div></section>
"""


def legal_page(filename, title):
    document = (MISC / filename).read_text(encoding="utf-8")
    match = re.search(r"(<article\b.*?</article>)", document, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError(f"No legal article found in {filename}")
    article = match.group(1)
    return f'<section class="section legal"><div class="container">{article}</div></section>', title


def minify_html(document):
    return re.sub(r">\s+<", "><", document).strip() + "\n"


def minify_css(path):
    css = path.read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    path.write_text(css.strip() + "\n", encoding="utf-8")


def write(route, title, description, content, minify):
    target = OUT / route.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    document = shared(title, description, content, "/" + route.strip("/") + ("/" if route else ""))
    target.write_text(minify_html(document) if minify else document, encoding="utf-8")


def main(minify=False):
    if OUT.exists():
        rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for directory in ("css", "js", "webfonts"):
        source = ROOT / "assets" / directory
        target = OUT / "assets" / directory
        target.mkdir()
        for file in source.iterdir():
            copy2(file, target / file.name)
            if minify and file.name == "site.css":
                minify_css(target / file.name)
    images = OUT / "assets" / "images"
    images.mkdir()
    for path in (
        "2021/03/logo.png", "2021/03/cropped-fav-32x32.png", "2021/03/natalia.jpg",
        "2021/03/refl-twarzy.jpg", "2021/03/tlo.png", "2021/03/tlo2.png",
        "2021/03/markus-spiske-IKvDKHWF_5w-unsplash-scaled.jpg", "2025/10/profilowe-zdjece.jpg",
        "2025/10/1_ewa.png", "2025/10/2_agata.png", "2025/10/IMG_3641.jpg", "2025/10/IMG_3634.jpg",
        "2025/10/21.png", "2025/10/24.png", "2025/10/22.png", "2025/10/27.png", "2025/10/3.png",
        "2025/10/2.jpg", "2025/10/14.png", "2025/10/8.png", "2025/10/12.png", "2025/10/19.png",
        "2025/10/3_kasia.png", "2025/10/4_Lila.png", "2025/10/1.png", "2025/10/4.png",
        "2025/10/5.png", "2025/10/6.png", "2025/10/7.png", "2025/10/9.png", "2025/10/10.png",
        "2025/10/11.png", "2025/10/13.png", "2025/10/15.png", "2025/10/16.png", "2025/10/17.png",
        "2025/10/18a.png", "2025/10/20.png", "2025/10/25.png", "2025/10/26.png", "2025/10/28.png", "2025/10/29.png",
    ):
        copy2(UPLOADS / path, images / Path(path).name)
    copy2(
        ROOT / "assets/images/zjecie_konsultacja-online.webp",
        images / "zjecie_konsultacja-online.webp",
    )
    write("", "Refleksolog z pasją", "Holistyczne terapie naturalne dla kobiet we Wrocławiu i online.", HOME, minify)
    write("oferta", "Oferta", "Holistyczne terapie naturalne we Wrocławiu i współpraca online.", OFFER, minify)
    write("o-mnie", "O mnie", "Poznaj Natalię Safjan, terapeutkę holistyczną i refleksolog.", ABOUT, minify)
    write("opinie", "Opinie", "Opinie klientek Dotyku Zdrowia.", REVIEWS, minify)
    privacy, privacy_title = legal_page("polityka_prywatnosci.html", "Polityka prywatności")
    rules, rules_title = legal_page("Regulamin_Newslettera.html", "Regulamin newslettera")
    write("polityka-prywatnosci", privacy_title, "Polityka prywatności Dotyku Zdrowia.", privacy, minify)
    write("regulamin-newslettera", rules_title, "Regulamin newslettera Dotyku Zdrowia.", rules, minify)
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://nataliadotykzdrowia.pl/sitemap.xml\n", encoding="utf-8")
    (OUT / "sitemap.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">""" + "".join(
        f"<url><loc>https://nataliadotykzdrowia.pl{path}</loc></url>"
        for path in ("/", "/oferta/", "/o-mnie/", "/opinie/", "/polityka-prywatnosci/", "/regulamin-newslettera/")
    ) + "</urlset>\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minify", action="store_true", help="Minify generated HTML and CSS.")
    main(**vars(parser.parse_args()))
