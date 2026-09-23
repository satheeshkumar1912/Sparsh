(() => {
  const doc = document;
  const body = doc.body;

  /* ——— Mobile & Tablet Off-Canvas Side Drawer Nav ——— */
  const nav = doc.querySelector("[data-primary-nav]");
  const toggle = doc.querySelector("[data-nav-toggle]");
  const closeBtn = doc.querySelector("[data-nav-close]");
  const backdrop = doc.querySelector("[data-nav-backdrop]");

  const setNav = (open) => {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    if (backdrop) {
      if (open) {
        backdrop.removeAttribute("hidden");
        // Force reflow for smooth opacity transition
        void backdrop.offsetWidth;
        backdrop.classList.add("is-active");
      } else {
        backdrop.classList.remove("is-active");
        setTimeout(() => {
          if (!nav.classList.contains("is-open")) {
            backdrop.setAttribute("hidden", "");
          }
        }, 360);
      }
    }
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (open) {
      doc.documentElement.style.overflow = "hidden";
      body.style.overflow = "hidden";
    } else {
      doc.documentElement.style.overflow = "";
      body.style.overflow = "";
    }
  };

  toggle && toggle.addEventListener("click", (e) => {
    e.stopPropagation();
    setNav(!nav.classList.contains("is-open"));
  });

  closeBtn && closeBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    setNav(false);
  });

  backdrop && backdrop.addEventListener("click", () => setNav(false));

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
    if (e.key === "Escape" && nav && nav.classList.contains("is-open")) {
      setNav(false);
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth >= 1200 && nav && nav.classList.contains("is-open")) {
      setNav(false);
    }
  }, { passive: true });

  /* ——— Nav dropdowns: open on hover/click, close when cursor leaves ——— */
  const dropdowns = doc.querySelectorAll("[data-nav-dropdown]");

  const setDropdownOpen = (item, open) => {
    const trigger = item.querySelector("[data-nav-dropdown-trigger]");
    item.classList.toggle("is-open", open);
    if (trigger) {
      trigger.setAttribute("aria-expanded", String(open));
      if (!open) trigger.blur();
    }
  };

  const closeAllDropdowns = (except = null) => {
    dropdowns.forEach((item) => {
      if (item !== except) setDropdownOpen(item, false);
    });
  };

  dropdowns.forEach((item) => {
    const trigger = item.querySelector("[data-nav-dropdown-trigger]");
    if (!trigger) return;

    item.addEventListener("mouseenter", () => {
      closeAllDropdowns(item);
      setDropdownOpen(item, true);
    });

    item.addEventListener("mouseleave", () => {
      setDropdownOpen(item, false);
    });

    trigger.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const willOpen = !item.classList.contains("is-open");
      closeAllDropdowns(item);
      setDropdownOpen(item, willOpen);
    });
  });

  doc.addEventListener("click", (e) => {
    dropdowns.forEach((item) => {
      if (!item.contains(e.target)) setDropdownOpen(item, false);
    });
  });

  doc.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeAllDropdowns();
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

  /* ——— Page-hero journey ambient (all inner pages) ——— */
  const initPageHeroAmbient = () => {
    doc.querySelectorAll(".page-hero").forEach((hero) => {
      if (hero.querySelector(".page-hero__ambient")) return;
      const wrap = doc.createElement("div");
      wrap.className = "page-hero__ambient";
      wrap.setAttribute("aria-hidden", "true");
      wrap.innerHTML = `
        <span class="page-hero__ambient-beam"></span>
        <span class="page-hero__ambient-beam"></span>
        <span class="page-hero__ambient-beam"></span>
        <svg class="page-hero__ambient-path" viewBox="0 0 1200 320" preserveAspectRatio="none" focusable="false">
          <path d="M-20,220 C180,180 280,280 420,210 S700,90 860,150 1040,240 1220,160"></path>
        </svg>
        <span class="page-hero__ambient-particle"></span>
        <span class="page-hero__ambient-particle"></span>
        <span class="page-hero__ambient-particle"></span>
        <span class="page-hero__ambient-particle"></span>
        <span class="page-hero__ambient-particle"></span>
        <span class="page-hero__ambient-particle"></span>
        <span class="page-hero__ambient-particle"></span>
        <span class="page-hero__ambient-particle"></span>
      `;
      hero.insertBefore(wrap, hero.firstChild);
    });
  };

  initPageHeroAmbient();

  /* ——— SPARSH Inclusive Education pathway infographic ——— */
  const initSparshPath = () => {
    const root = doc.querySelector("[data-sparsh-path]");
    if (!root) return;

    const nodes = Array.from(root.querySelectorAll("[data-sparsh-node]"));
    const dots = Array.from(root.querySelectorAll("[data-sparsh-dot]"));
    const wmLetters = Array.from(root.querySelectorAll("[data-wm-index]"));
    const panel = root.querySelector("[data-sparsh-panel]");
    const panelInner = root.querySelector("[data-sparsh-panel-inner]");
    const badge = root.querySelector("[data-sparsh-badge]");
    const letterFull = root.querySelector("[data-sparsh-letter-full]");
    const stepLabel = root.querySelector("[data-sparsh-step-label]");
    const titleEl = root.querySelector("[data-sparsh-title]");
    const textEl = root.querySelector("[data-sparsh-text]");
    const prevBtn = root.querySelector("[data-sparsh-prev]");
    const nextBtn = root.querySelector("[data-sparsh-next]");
    const progressPath = root.querySelector("[data-path-progress]");
    const traveler = root.querySelector("[data-path-traveler]");
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (!nodes.length || !panelInner || !titleEl || !textEl) return;

    let index = 0;
    let autoTimer = null;
    let userPaused = false;
    let pathLength = 0;

    if (progressPath) {
      pathLength = progressPath.getTotalLength();
      progressPath.style.strokeDasharray = String(pathLength);
      progressPath.style.strokeDashoffset = String(pathLength);
    }

    const pad = (n) => String(n).padStart(2, "0");

    const setProgressVisual = (i) => {
      if (!progressPath || !pathLength) return;
      const ratio = nodes.length <= 1 ? 1 : i / (nodes.length - 1);
      const offset = pathLength * (1 - ratio);
      progressPath.style.strokeDashoffset = String(offset);

      if (traveler) {
        const pt = progressPath.getPointAtLength(pathLength * ratio);
        traveler.setAttribute("cx", String(pt.x));
        traveler.setAttribute("cy", String(pt.y));
      }
    };

    const applyStep = (i, { animate = true } = {}) => {
      const node = nodes[i];
      if (!node) return;
      index = i;

      nodes.forEach((el, idx) => {
        const active = idx === i;
        el.classList.toggle("is-active", active);
        el.setAttribute("aria-selected", String(active));
        el.tabIndex = active ? 0 : -1;
      });

      dots.forEach((el, idx) => {
        el.classList.toggle("is-active", idx === i);
      });

      wmLetters.forEach((el, idx) => {
        el.classList.toggle("is-active", idx === i);
      });

      if (panel) {
        panel.setAttribute("aria-labelledby", node.id);
      }

      const letter = node.dataset.letter || "";
      const title = node.dataset.title || "";
      const text = node.dataset.text || "";

      const updateCopy = () => {
        if (badge) badge.textContent = letter;
        if (letterFull) letterFull.textContent = letter;
        if (stepLabel) stepLabel.textContent = `${pad(i + 1)} / ${pad(nodes.length)}`;
        titleEl.textContent = title;
        textEl.textContent = text;
        setProgressVisual(i);
      };

      if (!animate || reduceMotion) {
        updateCopy();
        return;
      }

      panelInner.classList.remove("is-entering");
      panelInner.classList.add("is-exiting");
      window.setTimeout(() => {
        updateCopy();
        panelInner.classList.remove("is-exiting");
        panelInner.classList.add("is-entering");
        // Force reflow so entering transition plays
        void panelInner.offsetWidth;
        panelInner.classList.remove("is-entering");
      }, 180);
    };

    const goTo = (i, { fromUser = false } = {}) => {
      const next = (i + nodes.length) % nodes.length;
      applyStep(next);
      if (fromUser) {
        userPaused = true;
        stopAuto();
        window.setTimeout(() => {
          userPaused = false;
          startAuto();
        }, 12000);
      }
    };

    const stopAuto = () => {
      if (autoTimer) {
        window.clearInterval(autoTimer);
        autoTimer = null;
      }
    };

    const startAuto = () => {
      stopAuto();
      if (reduceMotion || userPaused) return;
      autoTimer = window.setInterval(() => {
        goTo(index + 1);
      }, 4200);
    };

    nodes.forEach((node) => {
      node.addEventListener("click", () => {
        goTo(Number(node.dataset.index), { fromUser: true });
      });

      node.addEventListener("keydown", (e) => {
        let nextIndex = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") {
          nextIndex = index + 1;
        } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
          nextIndex = index - 1;
        } else if (e.key === "Home") {
          nextIndex = 0;
        } else if (e.key === "End") {
          nextIndex = nodes.length - 1;
        }
        if (nextIndex === null) return;
        e.preventDefault();
        goTo(nextIndex, { fromUser: true });
        nodes[(nextIndex + nodes.length) % nodes.length].focus();
      });

      node.addEventListener("mouseenter", () => {
        if (window.matchMedia("(hover: hover)").matches) {
          goTo(Number(node.dataset.index), { fromUser: true });
        }
      });
    });

    dots.forEach((dot) => {
      dot.addEventListener("click", () => {
        goTo(Number(dot.dataset.index), { fromUser: true });
      });
    });

    prevBtn && prevBtn.addEventListener("click", () => goTo(index - 1, { fromUser: true }));
    nextBtn && nextBtn.addEventListener("click", () => goTo(index + 1, { fromUser: true }));

    root.addEventListener("mouseenter", stopAuto);
    root.addEventListener("mouseleave", () => {
      if (!userPaused) startAuto();
    });
    root.addEventListener("focusin", stopAuto);
    root.addEventListener("focusout", (e) => {
      if (!root.contains(e.relatedTarget) && !userPaused) startAuto();
    });

    // Entrance: draw path then begin autoplay when in view
    const begin = () => {
      root.classList.add("is-drawn");
      applyStep(0, { animate: false });
      startAuto();
    };

    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              begin();
              io.disconnect();
            }
          });
        },
        { threshold: 0.35 }
      );
      io.observe(root);
    } else {
      begin();
    }
  };

  initSparshPath();
})();

