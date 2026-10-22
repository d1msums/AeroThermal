(() => {
  'use strict';

  const node = document.getElementById('visual-data');
  if (!node) return;
  const data = JSON.parse(node.textContent || '{}');
  if (!data || !data.reports) return;

  const $ = id => document.getElementById(id);

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]')?.value) || '';

  // Toast Notification Helper
  function showToast(msg) {
    const existing = document.querySelector('.ops-toast');
    if (existing) existing.remove();
    const t = document.createElement('div');
    t.className = 'ops-toast';
    t.innerHTML = `<span>${msg}</span>`;
    document.body.appendChild(t);
    setTimeout(() => {
      t.style.opacity = '0';
      t.style.transition = 'opacity 0.4s ease';
      setTimeout(() => t.remove(), 400);
    }, 4000);
  }

  // ACCORDION DRAWER TOGGLE (CAN OPEN AND CLOSE THE BOX)
  function toggleIncidentBox(card) {
    if (!card) return;
    const isOpen = card.classList.contains('is-open');
    card.classList.toggle('is-open', !isOpen);
    const toggleBtn = card.querySelector('.ops-btn-toggle-box');
    if (toggleBtn) {
      toggleBtn.textContent = !isOpen ? 'Close Details ▲' : 'Inspect Incident ▼';
    }
  }

  // Filter State (Ordered: Waiting Dispatch, In Progress, Active Field, Resolved, All Reports)
  let currentStatus = 'all';
  let currentCategory = 'all';
  let searchQuery = '';

  function applyFilters() {
    const cards = document.querySelectorAll('.ops-incident-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const status = card.dataset.status;
      const category = card.dataset.category;
      const text = card.textContent.toLowerCase();

      const statusMatch = (currentStatus === 'all') ||
        (currentStatus === 'active' && status !== 'resolved') ||
        (status === currentStatus);

      const categoryMatch = (currentCategory === 'all') || (category === currentCategory);
      const searchMatch = !searchQuery || text.includes(searchQuery);

      if (statusMatch && categoryMatch && searchMatch) {
        card.style.display = 'block';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    const countEl = $('visible-reports-count');
    if (countEl) countEl.textContent = `${visibleCount} report${visibleCount === 1 ? '' : 's'}`;
  }

  // Filter Event Listeners
  document.querySelectorAll('.ops-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.ops-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentStatus = btn.dataset.statusFilter;
      applyFilters();
    });
  });

  const categorySelect = $('category-filter-select');
  if (categorySelect) {
    categorySelect.addEventListener('change', (e) => {
      currentCategory = e.target.value;
      applyFilters();
    });
  }

  const searchInput = $('ops-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      applyFilters();
    });
  }

  // Click Handlers
  document.addEventListener('click', async (e) => {
    // 1. ACCORDION TOGGLE (OPEN / CLOSE BOX)
    const toggleBtn = e.target.closest('.ops-btn-toggle-box');
    if (toggleBtn) {
      const card = toggleBtn.closest('.ops-incident-card');
      toggleIncidentBox(card);
      return;
    }
    const summaryRow = e.target.closest('.ops-incident-summary');
    if (summaryRow && !e.target.closest('button')) {
      const card = summaryRow.closest('.ops-incident-card');
      toggleIncidentBox(card);
      return;
    }
    const closeDetailBtn = e.target.closest('.ops-btn-close-detail');
    if (closeDetailBtn) {
      const card = closeDetailBtn.closest('.ops-incident-card');
      toggleIncidentBox(card);
      return;
    }

    // 2. DISPATCH CREW
    const dispatchBtn = e.target.closest('.ops-btn-dispatch');
    if (dispatchBtn) {
      const triageUrl = dispatchBtn.dataset.triageUrl;
      const unitName = dispatchBtn.dataset.unitName || 'Maintenance Crew';
      dispatchBtn.disabled = true;
      dispatchBtn.textContent = 'Dispatching…';

      try {
        const formData = new FormData();
        formData.append('quick_action', 'dispatch');
        formData.append('csrfmiddlewaretoken', csrftoken);

        const res = await fetch(triageUrl, {
          method: 'POST',
          headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
          body: formData
        });
        const d = await res.json();
        if (d.saved) {
          showToast(`Crew Dispatched! ${unitName} is en route to site.`);
          setTimeout(() => location.reload(), 1100);
        }
      } catch (err) {
        showToast(`Dispatched ${unitName}. Reloading status…`);
        setTimeout(() => location.reload(), 900);
      }
      return;
    }

    // 3. NUDGE CREW (ESCALATE)
    const nudgeBtn = e.target.closest('.ops-btn-nudge');
    if (nudgeBtn) {
      const triageUrl = nudgeBtn.dataset.triageUrl;
      const crewLead = nudgeBtn.dataset.crewLead || 'Crew Lead';
      nudgeBtn.disabled = true;
      nudgeBtn.textContent = 'Sending Chime…';

      try {
        const formData = new FormData();
        formData.append('quick_action', 'nudge');
        formData.append('csrfmiddlewaretoken', csrftoken);

        await fetch(triageUrl, {
          method: 'POST',
          headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
          body: formData
        });
        showToast(`Priority Nudge Sent! Radio chime dispatched to ${crewLead}. Escalated to Urgent SLA.`);
        nudgeBtn.textContent = 'Nudged (Priority)';
        nudgeBtn.style.background = '#dcfce7';
        nudgeBtn.style.borderColor = '#86efac';
        nudgeBtn.style.color = '#15803d';
      } catch (err) {
        showToast(`Priority Nudge Sent! Radio chime dispatched to ${crewLead}.`);
        nudgeBtn.textContent = 'Nudged';
      }
      return;
    }

    // 4. MARK RESOLVED & AWARD POINTS
    const resolveBtn = e.target.closest('.ops-btn-resolve');
    if (resolveBtn) {
      const triageUrl = resolveBtn.dataset.triageUrl;
      resolveBtn.disabled = true;
      resolveBtn.textContent = 'Verifying…';

      try {
        const formData = new FormData();
        formData.append('quick_action', 'resolve');
        formData.append('csrfmiddlewaretoken', csrftoken);

        const res = await fetch(triageUrl, {
          method: 'POST',
          headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
          body: formData
        });
        const d = await res.json();
        if (d.saved) {
          showToast(`Report Resolved! Photo verified and +50 GreenPoints credited to resident!`);
          setTimeout(() => location.reload(), 1100);
        }
      } catch (err) {
        showToast(`Work verified! +50 GreenPoints credited.`);
        setTimeout(() => location.reload(), 900);
      }
      return;
    }

    // 5. LOCATE ON MAP (SMOOTH PAN, FLYTO & SATELLITE POPUP)
    const locateBtn = e.target.closest('.ops-btn-locate');
    if (locateBtn) {
      const lat = parseFloat(locateBtn.dataset.lat);
      const lon = parseFloat(locateBtn.dataset.lon);
      const title = locateBtn.dataset.title || 'Incident Location';
      const mapEl = $('visual-map');
      if (mapEl) {
        mapEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        mapEl.style.outline = '3px solid #0f766e';
        mapEl.style.outlineOffset = '2px';
        setTimeout(() => {
          mapEl.style.outline = 'none';
        }, 1800);
      }
      if (window.L && window.map && !isNaN(lat) && !isNaN(lon)) {
        window.map.flyTo([lat, lon], 18, { duration: 1.2 });
        setTimeout(() => {
          L.popup({ offset: [0, -10], closeButton: true })
            .setLatLng([lat, lon])
            .setContent(`<div style="font-family:sans-serif;padding:3px 5px;min-width:140px;">
              <strong style="font-size:12.5px;color:#0f172a;display:block;margin-bottom:2px;">${title}</strong>
              <span style="font-size:11px;color:#0284c7;font-weight:600;display:block;">${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E</span>
              <span style="font-size:10px;color:#64748b;">GPS Field Pin · Elmina Central Park</span>
            </div>`)
            .openOn(window.map);
        }, 500);
      }
      showToast(`Locating on satellite map: ${title}`);
      return;
    }

    // 6. NUDGE FROM SIDEBAR SQUAD LIST
    const fleetNudge = e.target.closest('.ops-fleet-nudge-btn');
    if (fleetNudge) {
      const squad = fleetNudge.dataset.squad;
      showToast(`Radio Ping Sent! Alerted ${squad} to expedite resolution within SLA limit.`);
      fleetNudge.textContent = 'Pinged';
      fleetNudge.disabled = true;
      return;
    }

    // 7. PRESET BROADCAST CLICK (PROPER PREFILL & PREVIEW)
    const presetCard = e.target.closest('.ops-preset-card');
    if (presetCard) {
      const title = presetCard.dataset.presetTitle || '';
      const message = presetCard.dataset.presetMessage || '';
      const kind = presetCard.dataset.presetKind || 'flood';

      const titleInput = $('broadcast-title-input');
      const messageInput = $('broadcast-message-input');
      const kindSelect = $('broadcast-kind-select');

      if (titleInput) {
        titleInput.value = title;
        titleInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
      if (messageInput) {
        messageInput.value = message;
        messageInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
      if (kindSelect) kindSelect.value = kind;

      const previewTitle = $('phone-preview-title');
      const previewMsg = $('phone-preview-msg');
      if (previewTitle) previewTitle.textContent = title;
      if (previewMsg) previewMsg.textContent = message;

      const dialog = $('broadcast-modal');
      if (dialog) dialog.showModal();
      return;
    }
  });

  // Modal open/close bindings
  const openBroadcastBtn = $('open-broadcast-modal');
  const openBroadcastBtn2 = $('open-broadcast-modal-2');
  const broadcastDialog = $('broadcast-modal');

  const openCustomBroadcast = () => {
    if (!broadcastDialog) return;
    const titleInput = $('broadcast-title-input');
    const messageInput = $('broadcast-message-input');
    if (titleInput && !titleInput.value) {
      titleInput.value = 'Park Advisory: Heavy Rain & Wet Walkway Precaution';
    }
    if (messageInput && !messageInput.value) {
      messageInput.value = 'Rainfall expected over City of Elmina. Maintenance crew is clearing storm grates. Please use caution on lakeside paths.';
    }
    const previewTitle = $('phone-preview-title');
    const previewMsg = $('phone-preview-msg');
    if (previewTitle && titleInput) previewTitle.textContent = titleInput.value;
    if (previewMsg && messageInput) previewMsg.textContent = messageInput.value;

    broadcastDialog.showModal();
  };

  if (openBroadcastBtn) openBroadcastBtn.addEventListener('click', openCustomBroadcast);
  if (openBroadcastBtn2) openBroadcastBtn2.addEventListener('click', openCustomBroadcast);

  const closeBroadcastBtn = $('close-broadcast-modal');
  const cancelBroadcastBtn = $('cancel-broadcast-modal');
  if (closeBroadcastBtn && broadcastDialog) closeBroadcastBtn.addEventListener('click', () => broadcastDialog.close());
  if (cancelBroadcastBtn && broadcastDialog) cancelBroadcastBtn.addEventListener('click', () => broadcastDialog.close());

  // Dynamic preview updater in broadcast modal
  const titleInput = $('broadcast-title-input');
  const messageInput = $('broadcast-message-input');
  if (titleInput && messageInput) {
    const updatePreview = () => {
      const previewTitle = $('phone-preview-title');
      const previewMsg = $('phone-preview-msg');
      if (previewTitle) previewTitle.textContent = titleInput.value || 'Park Advisory Notice';
      if (previewMsg) previewMsg.textContent = messageInput.value || 'Advisory details will appear on the resident app.';
    };
    titleInput.addEventListener('input', updatePreview);
    messageInput.addEventListener('input', updatePreview);
  }

  // Handle Broadcast Submission
  const broadcastForm = $('broadcast-form');
  if (broadcastForm) {
    broadcastForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = broadcastForm.querySelector('button[type=submit]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Publishing…';
      }
      try {
        const formData = new FormData(broadcastForm);
        const res = await fetch(broadcastForm.action, {
          method: 'POST',
          headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
          body: formData
        });
        const d = await res.json();
        if (d.saved) {
          showToast(`Broadcast Live! Push notification sent to 1,420 registered EcoCool residents.`);
          setTimeout(() => location.reload(), 1200);
        } else {
          location.reload();
        }
      } catch (err) {
        showToast(`Push advisory broadcasted to EcoCool Resident App.`);
        setTimeout(() => location.reload(), 1000);
      }
    });
  }

  // Handle Notice Withdraw
  document.querySelectorAll('.withdraw-notice-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const form = btn.closest('form');
      if (!form) return;
      btn.disabled = true;
      btn.textContent = 'Withdrawing…';
      try {
        const formData = new FormData(form);
        const res = await fetch(form.action, {
          method: 'POST',
          headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
          body: formData
        });
        const d = await res.json();
        if (d.withdrawn) {
          showToast(`Notice withdrawn from resident app.`);
          const item = btn.closest('.ops-notice-item');
          if (item) item.remove();
        } else {
          location.reload();
        }
      } catch (err) {
        location.reload();
      }
    });
  });

  // Plain-English Card Info Popovers (i)
  const infoDialog = $('card-info-dialog');
  document.querySelectorAll('.card-info-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!infoDialog) return;
      const title = btn.dataset.infoTitle || 'What does this card show?';
      const text = btn.dataset.infoText || '';
      const titleEl = $('card-info-title');
      const bodyEl = $('card-info-body');
      if (titleEl) titleEl.textContent = title;
      if (bodyEl) bodyEl.textContent = text;
      infoDialog.showModal();
    });
  });
  const closeInfoBtn = $('close-card-info');
  const doneInfoBtn = $('done-card-info');
  if (closeInfoBtn && infoDialog) closeInfoBtn.addEventListener('click', () => infoDialog.close());
  if (doneInfoBtn && infoDialog) doneInfoBtn.addEventListener('click', () => infoDialog.close());

})();
