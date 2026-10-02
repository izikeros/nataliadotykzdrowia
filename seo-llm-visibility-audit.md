# SEO and LLM Search Visibility Audit

**Website:** nataliadotykzdrowia.pl  
**Audited implementation:** `dotykzdrowia_static/`, source `build.py`, output `docs/`  
**Original audit:** 16 September 2026  
**Reassessment:** 29 September 2026

## Scope and limitations

This audit evaluates the generated static website against current technical SEO,
local SEO, health-content quality, structured-data, performance, accessibility,
and AI-assisted search discovery practices.

The reassessment covered:

- generated HTML pages,
- titles, descriptions, canonical URLs and headings,
- crawl controls and the XML sitemap,
- visible service and practitioner content,
- testimonial implementation,
- internal and external links,
- images, fonts, CSS and JavaScript,
- structured data and social metadata,
- content suitability for Google AI features and other answer engines,
- the standalone questionnaire at `/analiza.html`, both legal pages, and the
  homepage contact section at `/#kontakt`.

The audit does not include private Google Search Console, Bing Webmaster Tools,
Google Business Profile, analytics, backlink or production server data. Core Web
Vitals must also be measured on the deployed website because repository
inspection cannot determine production TTFB or field LCP, INP and CLS.
The checked-in `docs/` snapshot uses GitHub Pages project-path asset URLs;
`build.py` normally generates root-relative URLs for the custom domain. Neither
variant proves which output is currently deployed or how HTTP redirects,
response headers, indexing and firewall rules behave in production. `docs/` is
generated output, not a place to edit source content.

### Status of the original findings

| Finding                                                                  | Reassessment                                        | Evidence or qualification                                                                                                |
| ------------------------------------------------------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Directly readable Polish HTML, unique canonicals and descriptions        | Implemented for six primary routes                  | `build.py:64-80,263-270`; verify production responses separately                                                         |
| XML sitemap and permissive `robots.txt`                                  | Implemented for six routes                          | `build.py:271-275`; `/analiza.html` is not listed                                                                        |
| Contextual titles/descriptions and useful H1s                            | Still needs work                                    | Generic primary titles and short descriptions; legal pages have suitable descriptive headings                            |
| Local contact/entity details                                             | Still needs work                                    | `build.py:142` has phone, social links and booking, but no crawlable address or hours                                    |
| Open Graph, X cards and JSON-LD                                          | Still missing                                       | No corresponding markup in `build.py:64-117` or the questionnaire                                                        |
| Crawlable review text and image dimensions                               | Still missing                                       | `build.py:39-60,157-169`: 32 screenshots on reviews page, generic alt, no width/height                                   |
| AI-search readable answers and evidence-led health copy                  | Still needs work                                    | Existing health outcome claims; prioritize factual and safety review                                                     |
| WordPress pre-launch export and redirect preparation                     | Historical milestone, not a current pre-launch task | Check the historical URL inventory and live redirects before calling this complete                                       |
| Core Web Vitals, indexation, off-site profiles, production 404/redirects | Not verifiable in this repository                   | Require live HTTP checks, field data or account access                                                                   |
| `meta keywords`                                                          | Absent, not a required SEO fix                      | Google does not use this meta tag for web search ranking; research user intent and use relevant natural language instead |
| `llms.txt`                                                               | Missing, optional experiment                        | No proven search-ranking benefit; not a prerequisite for Google AI features                                              |

### Route inventory

| URL                       | Type                     | Notable exception                                                                                                                                                   |
| ------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/`                       | Canonical page           | Includes `/#kontakt` contact section, not a separate URL in sitemap                                                                                                 |
| `/o-mnie/`                | Canonical page           | Qualification details and health claims need evidence review                                                                                                        |
| `/oferta/`                | Canonical page           | One broad offer, with office and online sections                                                                                                                    |
| `/opinie/`                | Canonical page           | Review content is presented as images                                                                                                                               |
| `/polityka-prywatnosci/`  | Canonical legal page     | Legal copy is imported from the adjacent WordPress project; do not add artificial commercial keywords                                                               |
| `/regulamin-newslettera/` | Canonical legal page     | Same external source dependency as privacy policy                                                                                                                   |
| `/analiza.html`           | Standalone questionnaire | Has title and H1, but no description/canonical/OG/JSON-LD; not in sitemap. Decide whether public indexing is appropriate before recommending canonical or `noindex` |

## Executive assessment

The static site has a good technical foundation: clean pre-rendered HTML,
HTTPS canonical URLs, a Polish language declaration, responsive markup, valid
local links, `robots.txt`, and an XML sitemap. It is also substantially leaner
than the WordPress version.

Its main visibility constraint is no longer the platform. Search engines and
LLM-based search systems receive too little structured, verifiable information
about the practitioner, location, services, expertise and health claims.

| Area                             |                  Current state | Opportunity                     |
| -------------------------------- | -----------------------------: | ------------------------------- |
| Crawlability and basic HTML      |                           Good | Preserve                        |
| Titles and search snippets       |                           Weak | High                            |
| Local SEO                        |                      Very weak | Very high                       |
| Structured data                  |                        Missing | High                            |
| Health-content trust and E-E-A-T |                     Weak/risky | Critical                        |
| Content and query coverage       |                        Limited | Very high                       |
| LLM citation readiness           |                           Weak | High                            |
| Performance                      |      Reasonable, not optimized | Medium-high                     |
| Social sharing metadata          |                        Missing | Medium                          |
| Measurement                      | Not verifiable from repository | Essential for ongoing decisions |

## Current strengths

- Pages are generated as directly readable HTML rather than relying on
  client-side rendering.
- Each of the six primary pages has a unique canonical URL.
- The document language is correctly declared as Polish.
- A meta description exists on each of the six primary pages; the separately
  copied questionnaire has none.
- The build emits `robots.txt` and an XML sitemap for the six primary pages.
- Internal links resolve correctly in the generated build.
- The static implementation has very little JavaScript.
- Important content is generally visible without JavaScript.
- Main editorial images have useful alternative text and explicit dimensions.
- The existing build includes checks for generated routes, links and image budgets;
  the results of a previous run do not establish current production behavior.

These strengths should be preserved while the visibility improvements are
introduced.

## Highest-impact improvements

### 1. Establish a clear local business and practitioner entity

The site mentions Wrocław, but the crawlable contact section contains only a
phone number, social profiles and a booking link. It does not expose a full
business address, service area, opening hours, email, map link, business
identifiers or other consistent local-business information.

Add a proper contact and location section containing, where applicable:

- full business name and practitioner name,
- street address, postcode and city,
- phone number and contact method,
- opening hours or an explicit "visits by appointment" statement,
- link to the Google Business Profile or Google Maps listing,
- areas served,
- accessibility, parking and public transport information,
- consistent business data across the website and external profiles.

The same name, address and phone information should be maintained across:

- Google Business Profile,
- Bing Places,
- Apple Business Connect,
- Facebook and Instagram,
- booking profiles,
- relevant professional and local directories,
- the shop subdomain.

Add matching JSON-LD using conservative and truthful schema types:

- `LocalBusiness`, or the most accurate applicable subtype,
- `Person` for Natalia Safjan,
- `Service` for each real service,
- `WebSite`,
- `BreadcrumbList`,
- `sameAs` links to official profiles.

Where the information is publicly visible, include the address, coordinates,
telephone, opening hours, booking URL, images, service area and price range.

Do not use `MedicalBusiness`, medical credentials or medical specialties unless
they formally apply. Do not add `AggregateRating` merely from screenshots of
first-party testimonials. Self-serving local-business review markup is
generally not eligible for Google review stars.

### 2. Replace generic titles with search-intent titles

Several primary-page titles communicate little about the page before the brand suffix:

- `Oferta | Dotyk Zdrowia Natalia Safjan`
- `O mnie | Dotyk Zdrowia Natalia Safjan`
- `Opinie | Dotyk Zdrowia Natalia Safjan`

The homepage title, `Refleksolog z pasją`, omits the location and does not fully
describe the principal service.

Suggested starting points:

| Page    | Suggested title                                                          |
| ------- | ------------------------------------------------------------------------ |
| Home    | `Holistyczne terapie naturalne dla kobiet we Wrocławiu – Natalia Safjan` |
| Offer   | `Holistyczna terapia we Wrocławiu i współpraca online – oferta`          |
| About   | `Natalia Safjan – dyplomowana refleksolog we Wrocławiu`                  |
| Reviews | `Opinie klientek – refleksologia i terapie naturalne Wrocław`            |

These are editorial starting points, not prescriptions: do not imply a
standalone service that the page does not actually describe. The existing
legal-page titles identify their purpose and do not need commercial keywords.
Titles should remain natural and accurately match each page. Final wording
should be reviewed against actual search-query data after Search Console begins
collecting information.

Current primary-page meta descriptions are short and mostly generic. Expand
commercial-page descriptions into page-specific propositions that explain:

- what the service is,
- where it is available,
- who it is intended for,
- what differentiates the offer,
- what action the visitor can take.

Meta descriptions are not a direct ranking factor, but they can affect how the
result is presented and whether users click it.
The absent `<meta name="keywords">` is worth reporting as a literal absence
only. Do not add it as a purported Google ranking factor; use service and
location terminology naturally in page text, headings and links.

### 3. Make the main headings descriptive

The homepage H1 is emotionally engaging:

> Czujesz, że Twój organizm od dłuższego czasu wysyła Ci sygnały?

However, it does not identify the practitioner, location or service category.
Retain this message visually, but make the primary heading explicit, for
example:

> Refleksologia i indywidualne terapie naturalne dla kobiet we Wrocławiu

The existing question can become a supporting heading or introductory
statement.

The reviews-page H1 is a long explanatory sentence rather than a concise page
title. It should use a descriptive heading such as:

> Opinie klientek Dotyku Zdrowia

The existing sentence can remain as introductory copy beneath it.
The legal pages already have descriptive H1s; the standalone questionnaire
also has a descriptive H1, but its search-indexing intent should be decided
before any search-snippet optimization.

### 4. Address health and YMYL credibility before expanding content

Health is a high-trust, high-risk search category. The current copy includes
statements about:

- recovering from advanced pneumonia through cupping,
- reducing asthma symptoms,
- reducing migraines,
- improving well-being in depressive states,
- detecting blocked meridians,
- reaching causes of health problems,
- achieving "maximum therapeutic effect".

Unsupported treatment and outcome claims can weaken search visibility and user
trust, regardless of whether they are based on personal experiences.

Improve the content by:

- describing services as complementary support rather than diagnosis or a
  replacement for medical care,
- separating personal experiences from established clinical evidence,
- avoiding guarantees and language implying treatment of named diseases,
- adding contraindications and safety limitations,
- explaining when a visitor should consult a physician or another regulated
  professional,
- citing reputable primary or institutional sources for factual health claims,
- explaining where evidence is limited or uncertain,
- publishing complete and verifiable qualifications,
- adding a clear editorial and health-content review policy,
- identifying the author and, where appropriate, a qualified medical reviewer.

Qualifications should include the real institution, qualification name and year
where this information can be published. Professional memberships and
independently verifiable profiles should be linked when applicable.

### 5. Create focused service pages

The six-page static site has one broad commercial page covering several
substantially different services and visitor intents. A single `/oferta/` page
is unlikely to be the best landing page for every relevant query.

Create focused pages only for services genuinely offered. Possible information
architecture:

- `/refleksologia-wroclaw/`
- `/refleksologia-stop-wroclaw/`
- `/refleksologia-twarzy-i-glowy/`
- `/terapia-bankami-wroclaw/`
- `/terapia-holistyczna-wroclaw/`
- `/wspolpraca-holistyczna-online/`

Keep `/oferta/` as a concise overview linking to these service pages.

Each service page should explain:

- what the service is,
- what happens during a session,
- who it may and may not suit,
- contraindications and safety considerations,
- what outcomes can reasonably be expected,
- what available evidence does and does not show,
- duration and price,
- location or online format,
- practitioner qualifications,
- frequently asked questions,
- a direct booking action.

This structure creates better landing pages for conventional searches and for
the related-query expansion used by AI-assisted search systems.

### 6. Build a focused knowledge section

The current static site contains approximately:

- 550 crawlable words on the homepage,
- 713 words on the offer page,
- 322 words on the practitioner page,
- 105 words on the reviews page.

There is almost no crawlable educational content. A small, high-quality
knowledge section represents one of the largest sustainable organic visibility
opportunities.

Potential topics include:

- Jak wygląda pierwsza wizyta u refleksologa?
- Refleksologia stóp: na czym polega i czego można oczekiwać?
- Refleksologia a masaż stóp — różnice.
- Jak przygotować się do zabiegu?
- Jakie są przeciwwskazania do refleksologii?
- Jakie są przeciwwskazania do terapii bańkami?
- Co wiadomo z badań o refleksologii?
- Kiedy objawy wymagają konsultacji lekarskiej?
- Terapia w gabinecie a współpraca online.
- Jak wybrać refleksologa i zweryfikować kwalifikacje?

Each resource should use a reader-first structure:

1. A direct two- or three-sentence answer.
2. Supporting explanation.
3. Practical first-hand observations.
4. Limitations and safety information.
5. Sources.
6. Author, reviewer where needed, and a meaningful update date.

Do not mass-produce generic AI-generated articles or cover unrelated wellness
topics simply to gain traffic. A limited collection of original, useful,
well-sourced pages is more valuable than a high publishing volume.

### 7. Make testimonials machine-readable and accessible

The reviews page contains 32 testimonial screenshots but only approximately 105
crawlable words. Every screenshot currently uses the same alternative text:

```html
alt="Opinia klientki"
```

Consequences:

- search and answer engines cannot understand what customers said,
- screen-reader users receive no meaningful review content,
- there is little topical evidence connecting reviews with particular services,
- images without intrinsic dimensions may contribute to layout movement.

With the reviewers' consent, transcribe reviews into HTML and include:

- the review text,
- first name or appropriately anonymized attribution,
- service discussed,
- original platform,
- source link where available,
- review date,
- the screenshot as supporting evidence rather than the only content.

Do not selectively rewrite reviews or present reported health outcomes as
guaranteed evidence. Use appropriate image alternatives: meaningful text where
the image communicates information, or an empty `alt` value when the same
review is fully transcribed next to it.

### 8. Add social sharing metadata

The six generated primary pages contain a title, description and canonical URL,
but no Open Graph or Twitter/X card metadata. The questionnaire has neither
description nor canonical. Neither has `og:image`: the current logo and
editorial images are **not** an Open Graph preview image.

Add page-specific:

- `og:title`,
- `og:description`,
- `og:type`,
- `og:url`,
- `og:image`,
- `og:image:width`,
- `og:image:height`,
- `og:locale="pl_PL"`,
- `twitter:card`,
- `twitter:title`,
- `twitter:description`,
- `twitter:image`.

Prepare at least one high-quality 1200×630 sharing image. Important service
pages should ideally have their own relevant images.

### 9. Improve structured data

No generated page currently contains JSON-LD. Add structured data that exactly
matches visible content.

Recommended graph:

- the website as `WebSite`,
- the business as `LocalBusiness`,
- Natalia Safjan as `Person`,
- official profiles through `sameAs`,
- relevant pages as `WebPage`,
- individual offerings as `Service`,
- navigational hierarchy as `BreadcrumbList`.

Structured data should use stable `@id` identifiers so the website, business,
person and services form a connected entity graph.

Structured data must not:

- invent qualifications or business attributes,
- label complementary services as regulated medical care,
- include reviews that are not visibly presented,
- claim ratings assembled from incompatible or unverifiable sources,
- describe information that users cannot find on the page.

Validate changes with Schema.org Validator and Google's Rich Results Test. Not
every valid schema type produces a Google rich result; its broader value is
clarifying entities and relationships.

### 10. Improve image and font performance

The static implementation is relatively small in HTML and JavaScript, but
several avoidable costs remain:

- `tlo2.png` is approximately 1.6 MB,
- `tlo.png` is approximately 638 KB,
- 43 emitted image files include 32 screenshots used on `/opinie/`; active
  JPEG/PNG formats total approximately 5.86 MiB,
- Font Awesome is loaded globally for a small number of icons,
- Google Fonts creates an external rendering dependency,
- testimonial images lack intrinsic dimensions,
- responsive `srcset` and `sizes` are not used consistently,
- modern formats are not used consistently.

Measurements from `python3 image_audit.py --directory docs/assets/images`
on the reassessment date: `tlo.png` 1200×675, 637.9 KiB;
`tlo2.png` 1200×675, 1602.6 KiB; contact background
`markus-spiske-IKvDKHWF_5w-unsplash-scaled.jpg` 1707×2560, 361.4 KiB;
`1_ewa.png` 1170×997, 451.3 KiB; logo 748×172, 13.0 KiB.
The HTML declares a 300×69 display size for the header logo and 748×172 for
the contact copy. Intrinsic dimensions, HTML attributes, and transmitted
bytes are different measurements; real network transfers depend on caching.

Recommended changes:

- convert large backgrounds to AVIF and WebP with suitable fallbacks,
- size source images according to actual display requirements,
- generate responsive image variants,
- use `<picture>`, `srcset` and `sizes`,
- add `width` and `height` to every testimonial image,
- mark only the actual LCP image with `fetchpriority="high"`,
- lazy-load below-the-fold images,
- add `decoding="async"` where appropriate,
- replace Font Awesome with the few required inline SVG icons,
- self-host and subset Montserrat, or use a suitable system-font stack,
- configure Brotli or Gzip compression,
- use immutable caching for fingerprinted assets,
- keep HTML caching short enough to permit timely updates.

Run Lighthouse and PageSpeed Insights against the deployed site on mobile and
desktop. Confirm real Core Web Vitals in Search Console after sufficient field
data is available.

### 11. Verify URL preservation after the WordPress-to-static migration

The static site currently defines six routes and does not include an explicit
404 page or migration redirect map in this repository. These could be configured
at the host: their absence in source does **not** establish that production
redirects or 404 handling are broken.

Audit the completed or ongoing migration:

1. Obtain the historical WordPress URL inventory and current indexed URLs.
2. Confirm that equivalent content retained the exact URL.
3. Test one-to-one permanent redirects for changed URLs on the live host.
4. Avoid redirecting unrelated removed pages to the homepage.
5. Test the live 404 page and add a useful custom page if missing.
6. Check live HTTP/HTTPS, www/non-www and trailing-slash behavior.
7. Check canonical URLs, sitemap URLs and internal links on the deployed site.
8. Submit the sitemap and inspect representative URLs in Google Search Console
   and Bing Webmaster Tools.

Losing existing URLs, indexed content and inbound-link signals could outweigh
all other improvements.

### 12. Improve the XML sitemap

The current generated sitemap lists all six canonical routes; the separately
copied `/analiza.html` is absent. Decide whether the questionnaire is intended
for public indexing first, then either add it to the sitemap with suitable
metadata or make the exclusion intentional (a sitemap omission alone does not
prevent indexing). Improve the sitemap by:

- adding accurate `<lastmod>` dates when content meaningfully changes,
- adding every new indexable service and knowledge page,
- excluding redirecting, duplicate and non-canonical URLs,
- keeping sitemap URLs identical to canonical URLs,
- automatically rebuilding the sitemap from the route definitions.

Do not modify dates merely to create a false impression of freshness.

### 13. Strengthen internal linking

Internal links should connect:

- the homepage to every primary service,
- service pages to relevant safety and educational articles,
- educational articles back to the relevant service,
- service pages to the practitioner and qualification information,
- testimonials to the applicable service where appropriate,
- every page to clear location and contact information.

Use descriptive link text rather than repeated phrases such as "tutaj" or
"więcej". Internal links should help users understand what they will find after
following them.

### 14. Maintain identity across external systems

The booking system and online shop are hosted on separate domains or
subdomains. Maintain clear entity continuity:

- use the same business and practitioner names,
- use the same logo and contact information,
- link reciprocally where useful,
- reference the main website as the authoritative business site,
- ensure external profiles link to the most relevant landing page,
- avoid inconsistent service names and descriptions.

This consistency helps people and automated systems recognize that the website,
shop, booking service and social profiles represent the same entity.

## LLM and AI-assisted search optimization

There is no separate, proven "LLM ranking formula". Google's current guidance
states that AI Overviews and AI Mode use the same indexability and people-first
SEO foundations as standard Google Search. No additional AI-specific schema or
file is required.

### Practical AI-search strategy

- Keep important information in visible HTML text.
- Do not place essential facts only in screenshots, images or third-party
  widgets.
- State the practitioner, location, services, prices, qualifications and
  limitations consistently.
- Use descriptive headings and short, self-contained answer sections.
- Publish original first-hand experience that generic websites cannot provide.
- Cite reliable external evidence.
- Clearly distinguish facts, professional observations and personal
  experiences.
- Build legitimate third-party mentions and consistent business profiles.
- Keep structured data consistent with visible content.
- Use descriptive internal links between services, questions and the
  practitioner profile.
- Keep the shop, booking system and main website consistent.

Answer engines often retrieve and cite individual passages rather than
summarizing an entire page. Each important section should therefore be
understandable on its own without relying on a promotional introduction.

### Crawler controls

The existing `robots.txt` allows all compliant crawlers:

```text
User-agent: *
Allow: /
Sitemap: https://nataliadotykzdrowia.pl/sitemap.xml
```

This is compatible with broad search discovery. If crawler control becomes
necessary, distinguish between search discovery and model training.

For example, OpenAI documents:

- `OAI-SearchBot` for search discovery,
- `GPTBot` for model training,
- `ChatGPT-User` for user-initiated retrieval.

Allowing search discovery does not require allowing every model-training
crawler. Any policy should be intentional and should also be enforced
consistently at the CDN or firewall layer. A crawler allowed by `robots.txt`
must not then be accidentally blocked by hosting security rules.

### `llms.txt`

An `llms.txt` file can be added experimentally as a concise list of canonical,
authoritative resources. However:

- it is not an established search ranking standard,
- support among major answer engines is not universal,
- there is no reliable evidence that it improves rankings,
- it cannot compensate for poor content, weak entity data or missing citations.

Treat `llms.txt` as a low-priority convenience after the core SEO and content
work is complete.

### Content format for citation readiness

Useful answer-oriented sections should contain:

1. A question or descriptive heading.
2. A concise direct answer.
3. Supporting detail and practical context.
4. Limitations or uncertainty.
5. Safety advice where applicable.
6. Links to sources.
7. Author and review information.

Tables are helpful for genuine comparisons, but should not be inserted only to
target answer engines. FAQ content should answer real client questions and
remain visible on the page.

Do not treat FAQ structured data as a guaranteed Google rich-result feature.
Check current Google feature support before prioritizing any FAQ markup;
visible, useful answers remain valuable independently of markup.

## Authority and off-site visibility

Technical changes alone will not establish authority. Pursue legitimate
mentions and citations through:

- a complete and actively maintained Google Business Profile,
- Bing Places and Apple Business Connect,
- relevant professional associations,
- verifiable training institutions,
- local Wrocław directories with editorial standards,
- interviews, podcasts and expert contributions,
- partnerships with legitimate complementary-health businesses,
- local events and workshops,
- original resources that other websites have a reason to cite.

Avoid paid link schemes, mass directory submission, fabricated reviews and
generic guest-post networks. They create risk without building durable
credibility.

## Measurement plan

### Essential setup

- Verify the domain property in Google Search Console.
- Submit and monitor the XML sitemap.
- Verify the site in Bing Webmaster Tools.
- Connect and maintain Google Business Profile.
- Use privacy-compliant analytics after consent where required.
- Track booking-link clicks, phone clicks, contact actions and newsletter
  subscriptions.
- Preserve production access logs where practical.

### Search reporting

Monitor:

- indexed and excluded URLs,
- queries by service and local intent,
- impressions, clicks, CTR and average position,
- branded versus non-branded searches,
- pages gaining or losing visibility,
- Core Web Vitals,
- crawl errors and redirect issues,
- Google Business Profile views and actions,
- completed bookings and qualified enquiries.

Google reports AI Overview and AI Mode traffic within the Search Console `Web`
search type rather than as a fully separate report. Referral reporting from
other answer engines may also be incomplete, so business outcomes should be
measured instead of relying only on attributed AI visits.

### Suggested baseline

If a pre-migration baseline exists, recover it; otherwise capture a dated
current baseline rather than presenting retrospective estimates as measurements:

- last 16 months of Search Console data,
- current indexed-page count,
- top queries and pages,
- current organic bookings or enquiry rate,
- Google Business Profile performance,
- current backlinks and referring domains,
- current mobile Core Web Vitals.

Compare performance over consistent subsequent periods while accounting for
normal seasonality and the actual deployment date.

## Recommended implementation order

### Phase 0: Verify the deployed static version and migration

1. Compare historical WordPress URLs with current indexed and deployed URLs.
2. Test existing one-to-one redirects and fix confirmed gaps.
3. Check the live 404 response and page; add a custom page if missing.
4. Rewrite risky health claims.
5. Add full local contact and location information.
6. Improve titles, H1 headings and descriptions.
7. Optimize `tlo.png` and `tlo2.png`.
8. Verify canonical, response status and trailing-slash behavior on the live host.

### Phase 1: First visibility release

1. Add `WebSite`, `LocalBusiness`, `Person`, `Service` and breadcrumb JSON-LD.
2. Add Open Graph and Twitter/X metadata.
3. Complete and reconcile Google Business Profile information.
4. Verify Google Search Console and Bing Webmaster Tools.
5. Submit the sitemap and request indexing for representative pages.
6. Configure analytics and conversion events.

### Phase 2: Content and trust

1. Split the offer into focused service pages.
2. Publish complete, verifiable qualifications.
3. Add contraindication, safety and evidence sections.
4. Transcribe testimonials with consent.
5. Improve testimonial image accessibility.
6. Add clear practitioner and editorial attribution.

### Phase 3: Sustainable growth

1. Publish one high-quality question-led resource at a time.
2. Strengthen contextual internal links.
3. Earn relevant local and professional mentions.
4. Monitor queries and revise pages based on demonstrated visitor needs.
5. Maintain consistent entity information across all profiles and domains.

### Phase 4: Experimental AI discovery

1. Define an explicit AI crawler policy.
2. Optionally add `llms.txt`.
3. Monitor answer-engine referrals and manual brand citations.
4. Do not prioritize experimental files over content, local SEO or authority.

## Prioritized opportunity matrix

| Priority               | Improvement                                                |          Expected value | Effort |
| ---------------------- | ---------------------------------------------------------- | ----------------------: | -----: |
| Critical               | Rewrite unsupported health claims and add safety context   |               Very high | Medium |
| Critical if gaps exist | Verify historic URLs and fix missing live redirects        |               Very high | Medium |
| High                   | Add full local business information and reconcile profiles |               Very high | Medium |
| High                   | Create focused service pages                               |               Very high |   High |
| High                   | Improve titles, H1 headings and descriptions               |                    High |    Low |
| High                   | Add entity and service structured data                     |                    High | Medium |
| High                   | Publish verifiable qualifications and content attribution  |                    High | Medium |
| High                   | Transcribe testimonial content                             |                    High | Medium |
| Medium-high            | Optimize large images and responsive delivery              |                    High | Medium |
| Medium                 | Add social sharing metadata                                |                  Medium |    Low |
| Medium                 | Build authoritative educational resources                  |          High over time |   High |
| Medium                 | Improve internal linking                                   |             Medium-high |    Low |
| Medium                 | Add measurement and conversion tracking                    | Essential for decisions | Medium |
| Low                    | Add an experimental `llms.txt` file                        |               Uncertain |    Low |

## Overall conclusion

The static version is technically suitable for strong visibility, but currently
presents itself more like a small digital brochure than a fully defined,
trustworthy health-service entity.

The strongest opportunities are:

1. complete local and practitioner entity information,
2. safer and better-supported health content,
3. focused service landing pages,
4. crawlable reviews and qualifications,
5. useful question-led educational content,
6. consistent structured data and external profiles,
7. preserved URLs and improved performance.

These changes should deliver substantially more value than adding
AI-specific files or producing large volumes of generic content. A
page-by-page snapshot of the observed values and image dimensions is available
in the local, non-deployed `seo-llm-visibility-report.html`. It is not
automatically refreshed when the site changes.

## Primary references

- [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Essentials](https://developers.google.com/search/docs/essentials)
- [Google: Local business structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- [Google: General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Google: Title links](https://developers.google.com/search/docs/appearance/title-link)
- [Google: Why it does not use the keywords meta tag](https://developers.google.com/search/blog/2009/09/google-does-not-use-keywords-meta-tag)
- [Google: Snippets and meta descriptions](https://developers.google.com/search/docs/appearance/snippet)
- [Google: Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [Google: Search documentation changelog](https://developers.google.com/search/updates)
- [Schema.org](https://schema.org/)
- [OpenAI crawler documentation](https://platform.openai.com/docs/bots)
- [IndexNow documentation](https://www.indexnow.org/documentation)
