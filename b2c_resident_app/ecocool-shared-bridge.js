// EcoCool SDP B2C Prototype — Shared Navigation & State Bridge + iPhone 18 Pro Frame Sync

(function () {
  // If user opened a raw code.html directly in the top window, snap into the iPhone 18 Pro 2TB Showcase Stage!
  if (window.self === window.top && window.location.pathname.endsWith('code.html')) {
    const target = window.location.pathname + window.location.search;
    window.location.replace('/?screen=' + encodeURIComponent(target));
    return;
  }

  const ROUTES = {
    home: '/ecocool_home_dashboard_dynamic_weather_flood_alert/code.html',
    touchGrass: '/touch_grass_aesthetic_wellness_theme/code.html',
    coolWalk: '/coolwalk_shaded_high_ground_routes/code.html',
    report: '/report_microclimate_hotspots_aesthetic_wellness_theme/code.html',
    reportCare: '/community_microclimate_reporting_aesthetic_wellness_theme/code.html',
    ecoPoints: '/my_ecopoints_impact_aesthetic_wellness_theme/code.html',
    profile: '/resident_ecoprofile_aesthetic_wellness_theme/code.html',
  };

  if (!localStorage.getItem('ecocool_points')) {
    localStorage.setItem('ecocool_points', '340');
  }
  if (!localStorage.getItem('ecocool_sim_mode')) {
    localStorage.setItem('ecocool_sim_mode', 'normal');
  }
  if (!localStorage.getItem('ecocool_township')) {
    localStorage.setItem('ecocool_township', 'City of Elmina');
  }

  function getPoints() {
    return parseInt(localStorage.getItem('ecocool_points') || '340', 10);
  }

  function notifyParent() {
    if (window.parent && window.parent !== window) {
      window.parent.postMessage(
        {
          type: 'ECOCOOL_STATE',
          points: getPoints(),
          simMode: localStorage.getItem('ecocool_sim_mode') || 'normal',
          township: localStorage.getItem('ecocool_township') || 'City of Elmina',
          path: window.location.pathname,
        },
        '*'
      );
    }
  }

  function setPoints(val) {
    const safeVal = Math.max(0, parseInt(val, 10));
    localStorage.setItem('ecocool_points', String(safeVal));
    syncPointsUI();
    notifyParent();
  }

  function addPoints(delta) {
    setPoints(getPoints() + delta);
  }

  function syncPointsUI() {
    const pts = getPoints();
    const profilePts = document.getElementById('points-display');
    if (profilePts) profilePts.innerText = String(pts);

    document.querySelectorAll('span, div, h2').forEach((el) => {
      if (el.children.length === 0 && /^\d+\s*pts$/i.test(el.textContent.trim())) {
        if (el.textContent.trim() === '340 pts' || el.dataset.dynamicPts === 'true') {
          el.dataset.dynamicPts = 'true';
          el.textContent = pts + ' pts';
        }
      }
      if (
        el.tagName === 'H2' &&
        el.classList.contains('font-metric') &&
        (el.textContent.trim() === '250' || el.dataset.dynamicHeroPts === 'true')
      ) {
        el.dataset.dynamicHeroPts = 'true';
        el.textContent = String(pts);
      }
    });

    const modalBalance = document.querySelector('#ecoPointsModal .font-data.text-\\[36px\\]');
    if (modalBalance) {
      modalBalance.innerHTML =
        pts + ' <span class="font-label-md text-label-md text-charcoal font-bold">PTS</span>';
    }
  }

  function navigateTo(url) {
    window.location.href = url;
  }

  // Inject clean mobile viewport CSS inside the iframe so fixed bars align 100% and scrollbars are hidden
  const style = document.createElement('style');
  style.textContent = `
    html, body {
      scrollbar-width: none !important;
      -ms-overflow-style: none !important;
      overflow-x: hidden !important;
      width: 100% !important;
      max-width: 100% !important;
      display: block !important;
      margin: 0 !important;
    }
    html::-webkit-scrollbar, body::-webkit-scrollbar {
      display: none !important;
    }
    body > div, main, section {
      width: 100% !important;
      max-width: 100% !important;
      min-width: 0 !important;
      box-sizing: border-box !important;
    }
    header.fixed.top-0 {
      left: 0 !important;
      right: 0 !important;
      transform: none !important;
      max-width: 100% !important;
      width: 100% !important;
    }
    nav.fixed.bottom-0 {
      left: 0 !important;
      right: 0 !important;
      transform: none !important;
      max-width: 100% !important;
      width: 100% !important;
      padding-bottom: 18px !important;
      z-index: 40 !important;
    }
    div.fixed.inset-0 {
      z-index: 999 !important;
      align-items: center !important;
      justify-content: center !important;
      padding: 16px !important;
    }
    #reward-modal > div {
      border-radius: 24px !important;
      transform: none !important;
      margin: auto !important;
    }
  `;
  document.head.appendChild(style);

  // Allow parent iPhone 18 Pro stage (Left Sidebar Scenario Controller) to command the app live
  window.addEventListener('message', (event) => {
    const cmd = event.data;
    if (!cmd || cmd.type !== 'ECOCOOL_CMD') return;
    if (cmd.township) {
      localStorage.setItem('ecocool_township', cmd.township);
      if (typeof window.selectTownship === 'function') {
        window.selectTownship(cmd.township, '');
      }
    }
    if (cmd.simMode) {
      localStorage.setItem('ecocool_sim_mode', cmd.simMode);
      if (typeof window.switchBannerMode === 'function') {
        window.switchBannerMode(cmd.simMode);
      }
      const simNormalBtn = document.getElementById('sim-normal-btn');
      const simStormBtn = document.getElementById('sim-storm-btn');
      if (cmd.simMode === 'storm' && simStormBtn) simStormBtn.click();
      if (cmd.simMode === 'normal' && simNormalBtn) simNormalBtn.click();
      if (typeof window.selectRoute === 'function') {
        window.selectRoute(cmd.simMode === 'storm' ? 'highground' : 'shaded');
      }
    }
    if (cmd.addPts) {
      addPoints(cmd.addPts);
    }
    notifyParent();
  });

  document.addEventListener('DOMContentLoaded', () => {
    syncPointsUI();
    notifyParent();

    const path = window.location.pathname;
    const params = new URLSearchParams(window.location.search);

    // 1. Wire up all Bottom Navigation Bars across all 6 screens
    document.querySelectorAll('nav a').forEach((link) => {
      const text = link.textContent.replace(/\s+/g, ' ').trim().toLowerCase();
      link.addEventListener('click', (e) => {
        e.preventDefault();
        if (text.includes('home')) navigateTo(ROUTES.home);
        else if (text.includes('touch grass')) navigateTo(ROUTES.touchGrass);
        else if (text.includes('coolwalk')) navigateTo(ROUTES.coolWalk);
        else if (text.includes('report')) navigateTo(ROUTES.report);
        else if (text.includes('profile')) navigateTo(ROUTES.profile);
      });
    });

    // 2. Wire up Top AppBar Back Buttons
    document.querySelectorAll('header button').forEach((btn) => {
      const icon = btn.querySelector('.material-symbols-outlined');
      if (icon && icon.textContent.trim() === 'arrow_back') {
        btn.onclick = (e) => {
          e.preventDefault();
          if (path.includes('my_ecopoints')) {
            navigateTo(ROUTES.profile);
          } else if (path.includes('community_microclimate_reporting')) {
            navigateTo(ROUTES.report);
          } else {
            navigateTo(ROUTES.home);
          }
        };
      }
    });

    // 3. HOME DASHBOARD SPECIFIC WIRING
    if (path.includes('ecocool_home_dashboard')) {
      const avatarImg = document.querySelector('header img');
      if (avatarImg && avatarImg.parentElement) {
        avatarImg.parentElement.style.cursor = 'pointer';
        avatarImg.parentElement.addEventListener('click', () => navigateTo(ROUTES.profile));
      }

      const savedTownship = localStorage.getItem('ecocool_township');
      if (savedTownship && typeof window.selectTownship === 'function') {
        window.selectTownship(savedTownship, '');
      }
      const origSelectTownship = window.selectTownship;
      if (typeof origSelectTownship === 'function') {
        window.selectTownship = function (name, region) {
          localStorage.setItem('ecocool_township', name);
          origSelectTownship(name, region);
          notifyParent();
        };
      }

      const savedMode = localStorage.getItem('ecocool_sim_mode');
      if (savedMode && typeof window.switchBannerMode === 'function') {
        window.switchBannerMode(savedMode);
      }
      const origSwitchBanner = window.switchBannerMode;
      if (typeof origSwitchBanner === 'function') {
        window.switchBannerMode = function (mode) {
          localStorage.setItem('ecocool_sim_mode', mode);
          origSwitchBanner(mode);
          notifyParent();
        };
      }

      const normalBannerBtns = document.querySelectorAll('#bannerNormalMode button');
      if (normalBannerBtns.length > 0) {
        normalBannerBtns[0].addEventListener('click', () => {
          navigateTo(ROUTES.coolWalk + '?route=shaded');
        });
      }

      const stormBannerBtns = document.querySelectorAll('#bannerStormMode button');
      if (stormBannerBtns.length > 0) {
        stormBannerBtns[0].onclick = () => {
          navigateTo(ROUTES.coolWalk + '?route=highground');
        };
      }

      const previewBtn = document.querySelector('#elevatedTrailsShowcase button');
      if (previewBtn) {
        previewBtn.addEventListener('click', () => {
          navigateTo(ROUTES.coolWalk + '?route=shaded');
        });
      }

      const pods = document.querySelectorAll('.grid.grid-cols-4 > div[role="button"]');
      pods.forEach((pod) => {
        const label = pod.textContent.replace(/\s+/g, ' ').trim().toLowerCase();
        if (label.includes('coolwalk')) {
          pod.addEventListener('click', () => navigateTo(ROUTES.coolWalk));
        } else if (label.includes('touch grass')) {
          pod.addEventListener('click', () => navigateTo(ROUTES.touchGrass));
        } else if (label.includes('report')) {
          pod.addEventListener('click', () => navigateTo(ROUTES.report));
        }
      });

      const ecoModalBtn = document.querySelector('#ecoPointsModal button.bg-\\[\\#667C68\\]');
      if (ecoModalBtn) {
        ecoModalBtn.onclick = () => {
          navigateTo(ROUTES.ecoPoints);
        };
      }
    }

    // 4. COOLWALK SCREEN SPECIFIC WIRING
    if (path.includes('coolwalk_shaded_high_ground_routes')) {
      const requestedRoute = params.get('route');
      const simMode = localStorage.getItem('ecocool_sim_mode');
      if (typeof window.selectRoute === 'function') {
        if (requestedRoute && ['shaded', 'shortest', 'highground'].includes(requestedRoute)) {
          window.selectRoute(requestedRoute);
        } else if (simMode === 'storm') {
          window.selectRoute('highground');
        }
      }
    }

    // 5. REPORT SCREEN 1 (report_microclimate_hotspots_aesthetic_wellness_theme)
    if (path.includes('report_microclimate_hotspots_aesthetic_wellness_theme')) {
      const simNormalBtn = document.getElementById('sim-normal-btn');
      const simStormBtn = document.getElementById('sim-storm-btn');
      const stormBanner = document.getElementById('storm-advisory-banner');
      const drainageBadge = document.getElementById('drainage-priority-badge');
      const drainageCard = document.getElementById('drainage-card');

      function applyReportSimMode(mode) {
        localStorage.setItem('ecocool_sim_mode', mode);
        notifyParent();
        if (mode === 'storm') {
          if (simStormBtn) {
            simStormBtn.className =
              'px-2 py-0.5 rounded-lg text-[10px] font-bold bg-[#BA1A1A] text-white shadow-xs transition-all';
          }
          if (simNormalBtn) {
            simNormalBtn.className =
              'px-2 py-0.5 rounded-lg text-[10px] font-bold bg-transparent text-[#54634D] hover:bg-[#667C68]/10 transition-all';
          }
          if (stormBanner) stormBanner.classList.remove('hidden');
          if (drainageBadge) drainageBadge.classList.remove('hidden');
          if (drainageCard) drainageCard.click();
        } else {
          if (simNormalBtn) {
            simNormalBtn.className =
              'px-2 py-0.5 rounded-lg text-[10px] font-bold bg-[#667C68] text-white shadow-xs transition-all';
          }
          if (simStormBtn) {
            simStormBtn.className =
              'px-2 py-0.5 rounded-lg text-[10px] font-bold bg-transparent text-[#54634D] hover:bg-[#667C68]/10 transition-all';
          }
          if (stormBanner) stormBanner.classList.add('hidden');
          if (drainageBadge) drainageBadge.classList.add('hidden');
        }
      }

      if (simNormalBtn) simNormalBtn.addEventListener('click', () => applyReportSimMode('normal'));
      if (simStormBtn) simStormBtn.addEventListener('click', () => applyReportSimMode('storm'));

      if (localStorage.getItem('ecocool_sim_mode') === 'storm') {
        applyReportSimMode('storm');
      }

      const submitBtn = document.getElementById('submit-btn');
      if (submitBtn) {
        submitBtn.addEventListener('click', () => {
          addPoints(25);
        });
      }

      const viewStatusBtn = document.getElementById('view-status-btn');
      if (viewStatusBtn) {
        viewStatusBtn.onclick = () => {
          navigateTo(ROUTES.reportCare);
        };
      }

      const closeModalBtn = document.getElementById('close-modal-btn');
      if (closeModalBtn) {
        closeModalBtn.onclick = () => {
          navigateTo(ROUTES.home);
        };
      }
    }

    // 6. REPORT SCREEN 2 (community_microclimate_reporting_aesthetic_wellness_theme)
    if (path.includes('community_microclimate_reporting_aesthetic_wellness_theme')) {
      const form = document.getElementById('microclimateReportForm');
      if (form) {
        form.addEventListener('submit', () => {
          addPoints(25);
        });
      }
    }

    // 7. PROFILE SCREEN SPECIFIC WIRING
    if (path.includes('resident_ecoprofile_aesthetic_wellness_theme')) {
      window.currentPoints = getPoints();
      const origTriggerRedemption = window.triggerRedemption;
      if (typeof origTriggerRedemption === 'function') {
        window.triggerRedemption = function (title, cost, code) {
          window.currentPoints = getPoints();
          origTriggerRedemption(title, cost, code);
          setPoints(window.currentPoints);
        };
      }
      const redeemHeaderPill = document.querySelector('#redeem-section span.rounded-full');
      if (redeemHeaderPill) {
        redeemHeaderPill.style.cursor = 'pointer';
        redeemHeaderPill.title = 'Open full My EcoPoints & Rewards catalog';
        redeemHeaderPill.addEventListener('click', () => navigateTo(ROUTES.ecoPoints));
      }
    }

    // 8. MY ECOPOINTS SCREEN SPECIFIC WIRING
    if (path.includes('my_ecopoints_impact_aesthetic_wellness_theme')) {
      const origCompleteRedemption = window.completeRedemption;
      if (typeof origCompleteRedemption === 'function') {
        window.completeRedemption = function () {
          const costEl = document.getElementById('modal-item-cost');
          const cost = costEl ? parseInt(costEl.textContent, 10) || 150 : 150;
          addPoints(-cost);
          origCompleteRedemption();
        };
      }
    }
  });
})();
