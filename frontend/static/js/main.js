(() => {
  const doc = document;
  const body = doc.body;

  /* ——— Mobile dropdown nav ——— */
  const nav = doc.querySelector("[data-primary-nav]");
  const toggle = doc.querySelector("[data-nav-toggle]");
  const closeBtn = doc.querySelector("[data-nav-close]");

  const setNav = (open) => {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };

  toggle && toggle.addEventListener("click", (e) => {
    e.stopPropagation();
    setNav(!nav.classList.contains("is-open"));
  });

  closeBtn && closeBtn.addEventListener("click", () => setNav(false));

  doc.addEventListener("click", (e) => {
    if (!nav || !toggle) return;
    if (nav.classList.contains("is-open") && !nav.contains(e.target) && !toggle.contains(e.target)) {
      setNav(false);
    }
  });

  nav && nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setNav(false));
  });

  doc.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setNav(false);
  });

  /* ——— Clean up any legacy contrast settings ——— */
  try {
    localStorage.removeItem("sparsh-contrast");
    doc.documentElement.removeAttribute("data-contrast");
  } catch (_) {}

  /* ——— Floating Scroll to Top & Scroll Progress ——— */
  const scrollTopBtn = doc.querySelector("[data-scroll-top]");
  const scrollProgressBar = doc.getElementById("scroll-progress-bar");
  const siteHeader = doc.querySelector(".site-header");

  let isScrolling = false;
  const handleScroll = () => {
    const scrollY = window.scrollY || doc.documentElement.scrollTop;
    const docHeight = doc.documentElement.scrollHeight - window.innerHeight;

    // Toggle scroll to top button
    if (scrollTopBtn) {
      scrollTopBtn.classList.toggle("is-visible", scrollY > 260);
    }

    // Header scrolled elevation
    if (siteHeader) {
      siteHeader.classList.toggle("is-scrolled", scrollY > 20);
    }

    // Scroll progress indicator
    if (scrollProgressBar && docHeight > 0) {
      const progress = Math.min(100, Math.max(0, (scrollY / docHeight) * 100));
      scrollProgressBar.style.width = `${progress}%`;
    }

    isScrolling = false;
  };

  window.addEventListener(
    "scroll",
    () => {
      if (!isScrolling) {
        window.requestAnimationFrame(handleScroll);
        isScrolling = true;
      }
    },
    { passive: true }
  );

  handleScroll();

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
      const mainContent = doc.getElementById("main-content");
      if (mainContent) {
        mainContent.focus({ preventScroll: true });
      }
    });
  }

  /* ——— Smooth Anchor Link Navigation ——— */
  doc.querySelectorAll('a[href^="#"]:not([href="#"])').forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      const targetId = anchor.getAttribute("href");
      if (targetId && targetId.length > 1) {
        const targetEl = doc.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
          if (history.pushState) {
            history.pushState(null, null, targetId);
          }
        }
      }
    });
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

  /* ——— Quick Enquiry AJAX Form Handling & Instant Refresh ——— */
  const initEnquiryForms = () => {
    const forms = doc.querySelectorAll('.admissions-enquiry-form, form[data-track-form="home-enquiry"], form[data-track-form="admissions-page"]');

    forms.forEach((form) => {
      const card = form.closest(".form-card");
      const successBanner = card ? card.querySelector(".enquiry-success-banner") : null;
      const submitBtn = form.querySelector(".btn--enquiry-submit") || form.querySelector('button[type="submit"]');

      // Helper to clear error states
      const clearErrors = () => {
        form.querySelectorAll(".is-invalid").forEach((el) => el.classList.remove("is-invalid"));
        form.querySelectorAll(".has-error").forEach((el) => el.classList.remove("has-error"));
        form.querySelectorAll(".field-error-slot").forEach((slot) => {
          slot.innerHTML = "";
        });
        const globalErr = form.querySelector(".form-errors");
        if (globalErr) globalErr.remove();
      };

      // Helper to attach inline error message
      const showFieldError = (fieldName, message) => {
        const fieldWrap = form.querySelector(`[data-field-name="${fieldName}"]`);
        if (fieldWrap) {
          fieldWrap.classList.add("has-error");
          const input = fieldWrap.querySelector(".form-control, input, select, textarea");
          if (input) input.classList.add("is-invalid");

          const slot = fieldWrap.querySelector(".field-error-slot");
          if (slot) {
            slot.innerHTML = `
              <div class="field-error-msg" role="alert">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>${message}</span>
              </div>
            `;
          }
        }
      };

      // Clear error on input interaction
      form.querySelectorAll(".form-control, input, select, textarea").forEach((input) => {
        input.addEventListener("input", () => {
          input.classList.remove("is-invalid");
          const wrap = input.closest(".form-field");
          if (wrap) {
            wrap.classList.remove("has-error");
            const slot = wrap.querySelector(".field-error-slot");
            if (slot) slot.innerHTML = "";
          }
        });
      });

      // Submit listener
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        track(`form:${form.getAttribute("data-track-form") || "enquiry"}`);
        clearErrors();

        if (submitBtn) {
          submitBtn.classList.add("is-loading");
          submitBtn.disabled = true;
        }

        const formData = new FormData(form);
        formData.append("is_ajax", "1");

        try {
          const response = await fetch(form.action || window.location.href, {
            method: "POST",
            body: formData,
            headers: {
              "X-Requested-With": "XMLHttpRequest",
              "Accept": "application/json",
            },
          });

          const data = await response.json().catch(() => null);

          if (response.ok && data && data.success) {
            // Reset all form fields to blank
            form.reset();
            clearErrors();

            // Display success banner
            if (successBanner) {
              successBanner.hidden = false;
              if (data.message) {
                const textEl = successBanner.querySelector(".enquiry-success-banner__text");
                if (textEl) textEl.textContent = data.message;
              }
              // Smooth scroll into view
              successBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
          } else {
            // Handle validation errors
            if (data && data.errors) {
              let firstField = null;
              for (const [field, errList] of Object.entries(data.errors)) {
                if (field === "__all__") {
                  const banner = doc.createElement("div");
                  banner.className = "form-errors";
                  banner.setAttribute("role", "alert");
                  banner.innerHTML = `
                    <svg class="form-errors__icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                    <div>${errList.join(" ")}</div>
                  `;
                  form.prepend(banner);
                } else {
                  showFieldError(field, errList[0]);
                  if (!firstField) {
                    firstField = form.querySelector(`[name="${field}"]`);
                  }
                }
              }
              if (firstField) {
                firstField.focus();
              }
            } else {
              alert(data?.message || "An unexpected error occurred. Please try again.");
            }
          }
        } catch (err) {
          console.error("[Sparsh] Enquiry form submit error:", err);
          // Fallback to regular submit if fetch failed completely
          form.submit();
        } finally {
          if (submitBtn) {
            submitBtn.classList.remove("is-loading");
            submitBtn.disabled = false;
          }
        }
      });

      // "Send another enquiry" button handler
      if (card) {
        card.querySelectorAll(".enquiry-reset-btn").forEach((btn) => {
          btn.addEventListener("click", () => {
            form.reset();
            clearErrors();
            if (successBanner) successBanner.hidden = true;
            const firstInput = form.querySelector('input[name="child_name"]');
            if (firstInput) firstInput.focus();
          });
        });
      }
    });
  };

  initEnquiryForms();

  // Reset forms on bfcache restoration (back button navigation)
  window.addEventListener("pageshow", (e) => {
    if (e.persisted) {
      doc.querySelectorAll('.admissions-enquiry-form, form[data-track-form="home-enquiry"], form[data-track-form="admissions-page"]').forEach((f) => {
        f.reset();
      });
    }
  });
})();

