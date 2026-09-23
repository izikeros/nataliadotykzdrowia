(() => {
  const storage = window.localStorage;
  const consent = document.querySelector("[data-consent]");
  const newsletter = document.querySelector("[data-newsletter]");
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".site-nav");
  const scrollTop = document.querySelector("[data-scroll-top]");

  const setConsent = (choice) => {
    storage.setItem("dz-consent", choice);
    consent.hidden = true;
    if (choice === "all") scheduleNewsletter();
  };
  const scheduleNewsletter = () => {
    if (storage.getItem("dz-newsletter-dismissed") || !newsletter) return;
    window.setTimeout(() => newsletter.showModal(), 30000);
  };

  if (toggle)
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  if (!storage.getItem("dz-consent")) consent.hidden = false;
  else if (storage.getItem("dz-consent") === "all") scheduleNewsletter();
  document
    .querySelectorAll("[data-consent-choice]")
    .forEach((button) =>
      button.addEventListener("click", () =>
        setConsent(button.dataset.consentChoice),
      ),
    );
  document.querySelectorAll("[data-open-consent]").forEach((button) =>
    button.addEventListener("click", () => {
      consent.hidden = false;
    }),
  );
  document
    .querySelector("[data-close-newsletter]")
    ?.addEventListener("click", () => {
      storage.setItem("dz-newsletter-dismissed", "1");
      newsletter.close();
    });
  newsletter?.addEventListener("cancel", () =>
    storage.setItem("dz-newsletter-dismissed", "1"),
  );
  if (scrollTop) {
    const updateScrollTop = () => {
      scrollTop.hidden = window.scrollY < 300;
    };
    window.addEventListener("scroll", updateScrollTop, { passive: true });
    updateScrollTop();
  }
})();
