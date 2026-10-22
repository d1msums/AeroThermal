/* Interactive What-If Weather & Lake Action Simulator Bridge */
(() => {
  const root = document.getElementById('at-climate'), app = document.getElementById('app');
  if (!app) return;

  const base = `/projects/${app.dataset.projectId}/resilience/`;
  const el = id => document.getElementById(id);
  const set = (id, v) => { if (el(id)) el(id).textContent = v; };
  const vol = n => `${Number(n).toLocaleString('en-MY')} m³`;

  const SCENARIO_META = {
    normal: {
      img: '/static/resilience/illustrations/scen_normal.jpg?v=1',
      badge: '☀️ CLEAR & CALM',
      temp: '31.0°C (Feels 33°C)',
      rain: '0 mm/hr · 12 km/h wind',
      happens: 'Park walkways, drains, and lake water levels are calm and normal. Safe for families and outdoor walks.',
      capPct: 65,
      bufferM3: 35000,
      storedM3: 65000,
      pill: 'SAFE BUFFER',
      lakeBox: '💧 <b>Flood Risk: Low</b> — 35,000 m³ of empty room is ready to catch sudden rain.',
      title: 'Routine check — no emergency action needed',
      steps: [
        ['Lake Gate:', 'Keep Outlet Gate #02 in standard automatic mode (65% level).'],
        ['Field Crew:', 'Run routine morning sweep of lakeside drain grates.'],
        ['Resident App:', 'Show green "Safe Outdoor Hours" status on the mobile app.']
      ]
    },
    storm: {
      img: '/static/resilience/illustrations/scen_storm.jpg?v=1',
      badge: '⛈️ HEAVY MONSOON STORM',
      temp: '25.8°C (Heavy Rain)',
      rain: '85 mm/hr · 48 km/h gusts',
      happens: 'Sudden heavy downpour washes fallen leaves into perimeter drains and sends 27,000 m³ of stormwater rushing into the lake.',
      capPct: 88,
      bufferM3: 12000,
      storedM3: 88000,
      pill: '⛈️ HIGH WATER ALERT',
      lakeBox: '⚠️ <b>Flood Risk: High (88% Full)</b> — Without early draining, only 12,000 m³ of room is left!',
      title: '⚡ Urgent: Drain lake early & clear blocked drains!',
      steps: [
        ['Step 1 (Lake Gate):', 'Open Lake Gate #02 4 hours BEFORE storm hits to release 12,000 m³ safely.'],
        ['Step 2 (Drain Crew):', 'Clear wet leaves & twigs from North & Lakeside storm drain grates immediately.'],
        ['Step 3 (Resident App):', 'Send Flash-Flood & Wet Trail alert to residents on the mobile app.']
      ]
    },
    heat: {
      img: '/static/resilience/illustrations/scen_heat.jpg?v=1',
      badge: '🔥 EXTREME HEATWAVE',
      temp: '38.6°C (Surface 42°C)',
      rain: '0 mm/hr · UV Index 11 (Extreme)',
      happens: 'Unshaded concrete paths and benches heat up past 38.6°C between 11 AM and 4 PM, making open walkways unsafe for children and seniors.',
      capPct: 72,
      bufferM3: 28000,
      storedM3: 72000,
      pill: '🔥 HEAT COOLING MODE',
      lakeBox: '☀️ <b>Water Strategy: Hold High (72%)</b> — Keep lake full so water breeze cools the lakeside park.',
      title: '☀️ Keep lake water high & guide families to shaded paths',
      steps: [
        ['Step 1 (Lake Gate):', 'Keep outlet gate CLOSED to retain 72,000 m³ water for natural lakeside cooling.'],
        ['Step 2 (Park Misting):', 'Turn on automated turf sprinklers at 11:00 AM & 2:30 PM along lakeside paths.'],
        ['Step 3 (Resident App):', 'Alert residents to use shaded CoolWalk routes and avoid midday sun (11 AM–4 PM).']
      ]
    },
    drought: {
      img: '/static/resilience/illustrations/scen_drought.jpg?v=1',
      badge: '🌵 DRY SPELL / DROUGHT',
      temp: '35.4°C (Dry Air · 42% RH)',
      rain: '0 mm rain for 14 days',
      happens: 'Two weeks without rain causes park soil to crack and young trees to wilt. Lake water drops due to high daily evaporation.',
      capPct: 48,
      bufferM3: 52000,
      storedM3: 48000,
      pill: '🌵 SAVE WATER RESERVE',
      lakeBox: '💧 <b>Water Reserve: 48% Full</b> — Lock water gates to save remaining 48,000 m³ for tree watering.',
      title: '💧 Lock lake gates & water young park trees',
      steps: [
        ['Step 1 (Lake Gate):', 'Lock Outlet Gate #02 completely to stop water loss and protect the 48,000 m³ reserve.'],
        ['Step 2 (Tree Care):', 'Pump recycled lake water at 6:30 AM to water dry saplings & add woodchip mulch.'],
        ['Step 3 (Resident App):', 'Ask residents to report dry or wilting park trees via the mobile app.']
      ]
    },
    wind: {
      img: '/static/resilience/illustrations/scen_wind.jpg?v=1',
      badge: '🌬️ STRONG MONSOON WIND',
      temp: '27.5°C (Gusty Squalls)',
      rain: '35 mm/hr · 62 km/h wind gusts',
      happens: 'Strong 62 km/h monsoon wind gusts snap heavy branches across jogging paths and blow debris into the lake.',
      capPct: 70,
      bufferM3: 30000,
      storedM3: 70000,
      pill: '🌬️ WIND & TREE ALERT',
      lakeBox: '🌊 <b>Lake Buffer: 70% Full</b> — Pre-release 5,000 m³ in case wind squalls bring sudden heavy rain.',
      title: '🌳 Clear fallen branches & prepare lake for squall rain',
      steps: [
        ['Step 1 (Lake Gate):', 'Pre-drain 5,000 m³ from Lake Gate #02 to create a 35,000 m³ safety buffer.'],
        ['Step 2 (Tree Crew):', 'Send arborist & chainsaw crew to clear snapped branches on the jogging loop.'],
        ['Step 3 (Resident App):', 'Push High-Wind Warning advising joggers to stay clear of tall rain trees.']
      ]
    }
  };

  const sel = el('at-scenario');
  let editable = true;

  function renderScenarioUI(key) {
    const chosen = SCENARIO_META[key] ? key : 'normal';
    const meta = SCENARIO_META[chosen];

    if (sel) sel.value = chosen;
    document.querySelectorAll('.at-scen-pill').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.scen === chosen);
    });

    // Update Card 1: Photo, Badge, Temp, Rain/Wind & What Happens
    const imgEl = el('at-scenario-img');
    if (imgEl) imgEl.src = meta.img;
    set('at-weather-badge', meta.badge);
    set('at-temp-val', meta.temp);
    set('at-rain-val', meta.rain);
    set('at-what-happens-desc', meta.happens);

    // Update Card 2: Lake Water Level
    set('at-capacity', `${meta.capPct}% Full`);
    if (el('at-storage')) el('at-storage').value = meta.capPct;
    set('at-condition', meta.pill);
    set('at-buffer', vol(meta.bufferM3));
    set('at-stored', vol(meta.storedM3));
    const lakeBox = el('at-lake-impact-box');
    if (lakeBox) lakeBox.innerHTML = meta.lakeBox;

    // Update Card 3: 1-2-3 Solution Steps
    if (el('at-alert')) el('at-alert').dataset.tone = chosen;
    set('at-alert-title', meta.title);
    const stepsList = el('at-solution-steps');
    if (stepsList) {
      stepsList.replaceChildren();
      meta.steps.forEach((step, idx) => {
        const li = document.createElement('li');
        li.innerHTML = `<span class="step-num">${idx + 1}</span><div><strong>${step[0]}</strong> ${step[1]}</div>`;
        stepsList.appendChild(li);
      });
    }
  }

  async function refresh() {
    if (!root || !sel) return;
    const r = await fetch(base + 'snapshot/', {credentials: 'same-origin'});
    if (!r.ok) throw Error();
    const d = await r.json();
    editable = d.can_manage;
    renderScenarioUI(d.scenario || 'normal');
  }

  async function selectScenario(chosen) {
    renderScenarioUI(chosen);
    if (!editable) return;
    try {
      const csrfNode = document.querySelector('[name=csrfmiddlewaretoken]');
      await fetch(base + 'scenario/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'X-CSRFToken': csrfNode ? csrfNode.value : ''
        },
        body: new URLSearchParams({scenario: chosen})
      });
    } catch (_) {}
  }

  if (sel) {
    sel.addEventListener('change', () => selectScenario(sel.value));
    document.querySelectorAll('.at-scen-pill').forEach(btn => {
      btn.addEventListener('click', () => selectScenario(btn.dataset.scen));
    });
    renderScenarioUI('storm');
  }

  // Plain-English Info Buttons ('i')
  const infoDialog = el('card-info-dialog');
  if (infoDialog) {
    document.addEventListener('click', e => {
      const btn = e.target.closest('.card-info-btn');
      if (!btn) return;
      e.preventDefault();
      e.stopPropagation();
      set('card-info-title', btn.dataset.infoTitle || 'What does this card show?');
      set('card-info-body', btn.dataset.infoText || '');
      infoDialog.showModal();
    });
    ['close-card-info', 'done-card-info'].forEach(id => {
      if (el(id)) el(id).onclick = () => infoDialog.close();
    });
  }

  // 'How this page works' dialog
  const notesDialog = el('data-notes');
  if (notesDialog) {
    if (el('open-notes')) el('open-notes').onclick = () => notesDialog.showModal();
    ['close-notes', 'done-notes'].forEach(id => {
      if (el(id)) el(id).onclick = () => notesDialog.close();
    });
  }

  // Lake Gate Action Modal
  const gateDialog = el('gate-dispatch-dialog');
  if (gateDialog) {
    if (el('open-gate-dispatch-btn')) {
      el('open-gate-dispatch-btn').onclick = () => {
        if (el('gate-dispatch-toast')) el('gate-dispatch-toast').hidden = true;
        gateDialog.showModal();
      };
    }
    ['close-gate-dispatch', 'cancel-gate-dispatch'].forEach(id => {
      if (el(id)) el(id).onclick = () => gateDialog.close();
    });
    if (el('confirm-gate-dispatch')) {
      el('confirm-gate-dispatch').onclick = () => {
        if (el('gate-dispatch-toast')) el('gate-dispatch-toast').hidden = false;
      };
    }
  }
})();
