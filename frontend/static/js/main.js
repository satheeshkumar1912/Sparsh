(() => {
  const doc = document;
  const body = doc.body;

  /* ——— Mobile nav ——— */
  const nav = doc.querySelector("[data-primary-nav]");
  const toggle = doc.querySelector("[data-nav-toggle]");
  const closeBtn = doc.querySelector("[data-nav-close]");
  const backdrop = doc.querySelector("[data-nav-backdrop]");

  const setNav = (open) => {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (backdrop) {
      backdrop.hidden = !open;
    }
    body.style.overflow = open ? "hidden" : "";
    if (open) {
      const first = nav.querySelector("a, button");
      first && first.focus();
    }
  };

  toggle && toggle.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
  closeBtn && closeBtn.addEventListener("click", () => setNav(false));
  backdrop && backdrop.addEventListener("click", () => setNav(false));
  doc.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setNav(false);
  });

  /* ——— High contrast ——— */
  const contrastBtn = doc.querySelector("[data-contrast-toggle]");
  const stored = localStorage.getItem("sparsh-contrast");
  if (stored === "high") {
    doc.documentElement.setAttribute("data-contrast", "high");
    contrastBtn && contrastBtn.setAttribute("aria-pressed", "true");
  }
  contrastBtn &&
    contrastBtn.addEventListener("click", () => {
      const on = doc.documentElement.getAttribute("data-contrast") !== "high";
      doc.documentElement.setAttribute("data-contrast", on ? "high" : "normal");
      contrastBtn.setAttribute("aria-pressed", String(on));
      localStorage.setItem("sparsh-contrast", on ? "high" : "normal");
    });

  /* ——— Accordion ——— */
  doc.querySelectorAll("[data-accordion]").forEach((root) => {
    root.querySelectorAll("[data-accordion-trigger]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const expanded = btn.getAttribute("aria-expanded") === "true";
        const panel = doc.getElementById(btn.getAttribute("aria-controls"));
        btn.setAttribute("aria-expanded", String(!expanded));
        if (panel) panel.hidden = expanded;
        const icon = btn.querySelector(".faq-item__icon");
        if (icon) icon.textContent = expanded ? "+" : "–";
      });
    });
  });

  /* ——— Reveal on scroll ——— */
  const reveals = doc.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  /* ——— Animated counters ——— */
  const counters = doc.querySelectorAll("[data-count]");
  const animateCount = (el) => {
    const target = Number(el.getAttribute("data-count") || 0);
    const duration = 1400;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased).toLocaleString("en-IN");
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  if (counters.length && "IntersectionObserver" in window) {
    const cio = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            cio.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((el) => cio.observe(el));
  } else {
    counters.forEach(animateCount);
  }

  /* ——— Privacy-compliant CTA analytics (no cookies; local queue) ——— */
  const queueKey = "sparsh-analytics-queue";
  const track = (name, detail = {}) => {
    const event = {
      name,
      detail,
      path: location.pathname,
      ts: new Date().toISOString(),
    };
    try {
      const q = JSON.parse(sessionStorage.getItem(queueKey) || "[]");
      q.push(event);
      sessionStorage.setItem(queueKey, JSON.stringify(q.slice(-100)));
    } catch (_) {
      /* ignore */
    }
    if (window.sparshAnalytics && typeof window.sparshAnalytics === "function") {
      window.sparshAnalytics(event);
    }
    if (location.search.includes("debugAnalytics")) {
      console.info("[Sparsh analytics]", event);
    }
  };

  doc.querySelectorAll("[data-track]").forEach((el) => {
    el.addEventListener("click", () => track(el.getAttribute("data-track")));
  });

  doc.querySelectorAll("[data-track-form]").forEach((form) => {
    form.addEventListener("submit", () => track(`form:${form.getAttribute("data-track-form")}`));
  });
})();
