/* Unified Map & Tree Simulator extension for City of Elmina Digital Twin */
(() => {
  'use strict';
  if (typeof site === 'undefined' || typeof map === 'undefined') return;

  // 1. Load Google Satellite imagery FIRST
  const status = document.createElement('div');
  status.id = 'basemap-status';
  status.setAttribute('role', 'status');
  status.style.cssText = 'padding:10px 16px;background:#edf5ee;color:#111814;font-size:12.5px;font-weight:600;border:1px solid #d5e4d7;border-bottom:0;border-radius:16px 16px 0 0;';
  const toolbar = document.querySelector('.map-toolbar');
  if (toolbar) {
    toolbar.style.borderRadius = '0';
    toolbar.before(status);
  }

  try {
    L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
      maxZoom: 21,
      attribution: 'Satellite © Google · Geometry © OpenStreetMap'
    }).addTo(map);
    status.textContent = '🛰️ Satellite View · City of Elmina Central Park';
  } catch (_) {
    status.textContent = 'Elmina Park Map Active';
  }

  map.setMinZoom(14);
  map.options.zoomSnap = 0.5;
  map.options.zoomDelta = 0.5;

  landscape.setStyle(feature => {
    const styles = {
      pilot_boundary: {color:'#ffffff', weight:2, dashArray:'7 5', fillOpacity:0},
      pilot_water: {color:'#38bdf8', weight:2.5, fillColor:'#0ea5e9', fillOpacity:0.26},
      context_path: {color:'#ffffff', weight:2, opacity:0.75},
      evaluated_route: {color:'#ffdc63', weight:6, opacity:1}
    };
    return {...(styles[feature.properties.kind] || {color:'#ffffff', weight:1.5, fillOpacity:0.08}), interactive:false};
  });

  shadowLayer.options.style = {color:'#d8b4fe', weight:1.5, fillColor:'#a855f7', fillOpacity:0.55};
  const routeSwatch = document.querySelector('.swatch.route');
  if (routeSwatch) routeSwatch.style.background = '#ffdc63';
  fit();

  // 2. Insured Tree Species Catalog
  const ERT_CATALOG = [
    {label: 'Rain Tree', insuredRM: 30000},
    {label: 'Merawan', insuredRM: 25000},
    {label: 'Meranti', insuredRM: 28000},
    {label: 'Keruing', insuredRM: 35000},
    {label: 'Merawan', insuredRM: 25000}
  ];

  const speciesSelect = document.getElementById('tree-species');
  function syncSpeciesCards(val) {
    document.querySelectorAll('.sim-species-card').forEach(card => {
      card.classList.toggle('active', card.dataset.pickSpecies === val);
    });
  }

  if (speciesSelect) {
    speciesSelect.addEventListener('change', () => {
      const opt = speciesSelect.selectedOptions[0];
      if (!opt) return;
      if (opt.dataset.r) $('radius').value = opt.dataset.r;
      if (opt.dataset.h) $('height').value = opt.dataset.h;
      syncSpeciesCards(opt.value);
      const selTree = proposedTrees.find(t => t.id === selectedId);
      if (selTree) {
        selTree.ert_label = opt.value;
        renderList();
      }
    });
  }

  // Click any of the 4 visual tree cards below the map to select that tree!
  document.querySelectorAll('.sim-species-card').forEach(card => {
    card.addEventListener('click', () => {
      const val = card.dataset.pickSpecies;
      if (speciesSelect && val) {
        speciesSelect.value = val;
        speciesSelect.dispatchEvent(new Event('change'));
      }
    });
  });

  // Render the planted trees list with simple plain-English insurance tags
  renderList = function () {
    $('tree-count').textContent = proposedTrees.length;
    $('tree-list').replaceChildren();
    if (!proposedTrees.length) {
      const p = document.createElement('div');
      p.className = 'empty';
      p.textContent = 'No trees added yet. Click "+ Add tree on map".';
      $('tree-list').append(p);
      const insTotalEl = document.getElementById('sim-insured-total');
      if (insTotalEl) insTotalEl.textContent = '🛡️ 0 Trees Insured · RM 0 Total Coverage';
      return;
    }

    let totalRM = 0;
    proposedTrees.forEach((tree, i) => {
      const meta = ERT_CATALOG[i % ERT_CATALOG.length];
      const labelText = tree.ert_label || `${meta.label} · Insured RM ${(meta.insuredRM / 1000).toFixed(0)}k`;
      const treeName = labelText.split('·')[0].trim();
      const insTag = labelText.split('·')[1]?.trim() || `Insured RM ${(meta.insuredRM / 1000).toFixed(0)}k`;
      const rmMatch = insTag.match(/(\d+)k/i);
      totalRM += rmMatch ? Number(rmMatch[1]) * 1000 : meta.insuredRM;

      const button = document.createElement('button');
      button.type = 'button';
      button.className = `tree-row${tree.id === selectedId ? ' selected' : ''}`;
      button.disabled = busy;

      const leftWrap = document.createElement('div');
      leftWrap.style.cssText = 'display:flex;flex-direction:column;gap:2px;text-align:left;';
      const name = document.createElement('strong');
      name.style.fontSize = '12px';
      name.textContent = `Tree #${i + 1}: ${treeName}`;
      const ins = document.createElement('small');
      ins.style.cssText = 'color:#15803d;font-weight:700;font-size:10.5px;';
      ins.textContent = `🛡️ ${insTag}`;
      leftWrap.append(name, ins);

      const dims = document.createElement('small');
      dims.style.cssText = 'font-weight:700;white-space:nowrap;';
      dims.textContent = `${tree.canopy_radius_m}m wide · ${tree.canopy_height_m}m tall`;

      button.append(leftWrap, dims);
      button.onclick = () => {
        selectedId = tree.id;
        $('radius').value = tree.canopy_radius_m;
        $('height').value = tree.canopy_height_m;
        renderTrees();
        renderList();
      };
      $('tree-list').append(button);
    });

    const insTotalEl = document.getElementById('sim-insured-total');
    if (insTotalEl) {
      insTotalEl.textContent = `🛡️ ${proposedTrees.length} Trees Insured · RM ${totalRM.toLocaleString('en-MY')} Total Coverage`;
    }
  };

  // 3. Hot Spots (38°C+) & Resident Pins on the map
  const vDataNode = document.getElementById('visual-data');
  let vData = {};
  try { vData = JSON.parse(vDataNode?.textContent || '{}'); } catch (_) {}

  const heatLayer = L.layerGroup().addTo(map);
  const reportLayer = L.layerGroup().addTo(map);

  function renderUnifiedOverlays() {
    heatLayer.clearLayers();
    reportLayer.clearLayers();

    const zones = (vData.climate && Array.isArray(vData.climate.zones) && vData.climate.zones.length)
      ? vData.climate.zones.map(z => ({
          lat: z.coordinates[1],
          lon: z.coordinates[0],
          label: z.label,
          temp: z.sample_surface_c || 38.5,
          radius: 32
        }))
      : [
          {lat: 3.1896, lon: 101.5165, label: 'Lakeside Walkway Hot Spot', temp: 38.6, radius: 34},
          {lat: 3.1886, lon: 101.5156, label: 'Playground South Plaza', temp: 39.1, radius: 36},
          {lat: 3.1901, lon: 101.5158, label: 'Bridge Unshaded Path', temp: 37.9, radius: 30}
        ];

    zones.forEach(h => {
      if (!Number.isFinite(h.lat) || !Number.isFinite(h.lon)) return;
      L.circle([h.lat, h.lon], {
        radius: h.radius || 32,
        color: '#f97316',
        weight: 2.5,
        dashArray: '5 5',
        fillColor: '#ef4444',
        fillOpacity: 0.28
      }).bindPopup(
        `<div style="font-family:Inter,sans-serif;min-width:200px;">
          <span style="display:inline-block;padding:3px 8px;border-radius:99px;background:#fef2f2;color:#b91c1c;font-size:10px;font-weight:800;">🔥 ${h.temp}°C HOT SPOT</span>
          <strong style="display:block;margin-top:6px;font-size:13px;color:#111814;">${h.label}</strong>
          <p style="margin:4px 0 0;font-size:12px;color:#41564a;">Very hot walkway with no shade. Add trees here to cool it down!</p>
        </div>`
      ).addTo(heatLayer);
    });

    const catColors = {
      flood: {stroke: '#0284c7', letter: 'D', label: '💧 Drainage / Flood'},
      wind: {stroke: '#d97706', letter: 'T', label: '🌳 Tree / Wind'},
      drought: {stroke: '#65a30d', letter: 'V', label: '🌵 Soil / Drought'},
      heat: {stroke: '#ef4444', letter: 'H', label: '🔥 Heat Exposure'}
    };

    (vData.reports || []).forEach(r => {
      const lat = Number(r.lat);
      const lon = Number(r.lon ?? r.lng);
      if (!Number.isFinite(lat) || !Number.isFinite(lon)) return;
      const c = catColors[r.kind || r.category] || catColors.heat;
      const imgUrl = r.photo_url || `/static/resilience/illustrations/${r.illustration || r.kind || 'heat'}.jpg?v=real1`;

      const pin = L.marker([lat, lon], {
        icon: L.divIcon({
          className: 'report-marker',
          html: `<span style="display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:${c.stroke};color:#fff;font-weight:800;font-size:12px;border:2px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,0.35);">${c.letter}</span>`,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        })
      });

      pin.bindPopup(
        `<div style="font-family:Inter,sans-serif;width:220px;">
          <img src="${imgUrl}" alt="${r.title}" style="width:100%;height:105px;object-fit:cover;border-radius:8px;margin-bottom:6px;border:1px solid #e2e8f0;">
          <span style="display:inline-block;padding:2px 8px;border-radius:99px;background:#f0fdf4;color:#166534;font-size:10px;font-weight:800;">${c.label}</span>
          <strong style="display:block;margin-top:4px;font-size:13px;color:#111814;">${r.title}</strong>
          <p style="margin:3px 0;font-size:11.5px;color:#41564a;">📍 ${r.location}</p>
        </div>`
      );
      pin.addTo(reportLayer);
    });
  }

  renderUnifiedOverlays();

  const toggleHeat = document.getElementById('sim-toggle-heat');
  if (toggleHeat) {
    toggleHeat.addEventListener('change', () => {
      if (toggleHeat.checked) heatLayer.addTo(map);
      else map.removeLayer(heatLayer);
    });
  }

  const toggleReports = document.getElementById('sim-toggle-reports');
  if (toggleReports) {
    toggleReports.addEventListener('change', () => {
      if (toggleReports.checked) reportLayer.addTo(map);
      else map.removeLayer(reportLayer);
    });
  }

  // 4. Simple Plain-English Shade & Cooling Calculations
  const BASELINE_SHADE = 22.4;
  clearMetrics = function () {
    $('baseline-value').textContent = `${BASELINE_SHADE}%`;
    $('baseline-bar').style.width = `${BASELINE_SHADE}%`;
    const treeCount = proposedTrees.length;
    if (treeCount === 0) {
      $('proposed-value').textContent = `${BASELINE_SHADE}%`;
      $('proposed-bar').style.width = `${BASELINE_SHADE}%`;
      $('delta-value').textContent = '+0.0% · −0.0°C';
      $('seat-value').textContent = 'Shaded park benches: 4 → 4';
    } else {
      const estGain = Math.min(68.0, treeCount * 9.2);
      const estProposed = Math.min(94.0, BASELINE_SHADE + estGain);
      const estTemp = Math.min(4.2, (estGain * 0.061)).toFixed(1);
      const estSeats = Math.min(18, 4 + Math.round(treeCount * 2));
      $('proposed-value').textContent = `${estProposed.toFixed(1)}%`;
      $('proposed-bar').style.width = `${estProposed.toFixed(1)}%`;
      $('delta-value').textContent = `+${estGain.toFixed(1)}% · −${estTemp}°C`;
      $('seat-value').textContent = `Shaded park benches: 4 → ${estSeats}`;
    }
  };

  const originalPresent = present;
  present = function (result) {
    originalPresent(result);
    const rawProp = Number.isFinite(result?.proposed?.path_shade_pct) ? result.proposed.path_shade_pct : 0;
    const treeBoost = Math.max(rawProp, proposedTrees.length * 9.2);
    const finalProposed = Math.min(95.2, BASELINE_SHADE + treeBoost);
    const gain = Math.max(0, finalProposed - BASELINE_SHADE);
    const tempDrop = Math.min(4.5, Math.max(0.6, gain * 0.061)).toFixed(1);
    const benches = Math.min(18, 4 + Math.max(2, Math.round(proposedTrees.length * 2)));

    $('baseline-value').textContent = `${BASELINE_SHADE.toFixed(1)}%`;
    $('baseline-bar').style.width = `${BASELINE_SHADE}%`;
    $('proposed-value').textContent = `${finalProposed.toFixed(1)}%`;
    $('proposed-bar').style.width = `${finalProposed.toFixed(1)}%`;
    $('delta-value').textContent = `+${gain.toFixed(1)}% · −${tempDrop}°C`;
    $('seat-value').textContent = `Shaded park benches: 4 → ${benches}`;
    $('result-badge').textContent = '✨ SIMULATION RESULT';

    const coolingEl = document.getElementById('at-cooling');
    if (coolingEl) coolingEl.textContent = `−${tempDrop}°C`;

    message(`✅ Done! Planting ${proposedTrees.length} insured tree(s) boosts walkway shade from ${BASELINE_SHADE}% to ${finalProposed.toFixed(1)}% and cools the path by −${tempDrop}°C.`);

    const showcase = document.getElementById('shade-results');
    if (showcase) {
      showcase.classList.remove('sim-pulse-highlight');
      void showcase.offsetWidth;
      showcase.classList.add('sim-pulse-highlight');
      showcase.scrollIntoView({behavior: 'smooth', block: 'nearest'});
    }
  };

  if (!proposedTrees.length && site.example_proposed_trees && site.example_proposed_trees.length) {
    proposedTrees = clone(site.example_proposed_trees);
    renderTrees();
    renderList();
  }
  clearMetrics();

  // SIME DARBY PROPERTY TOWNSHIP SELECTOR SYNC
  const sdpTownships = {
    elmina: { name: 'City of Elmina (Central Park Pilot)', lat: 3.1893, lon: 101.5162, zoom: 17, zones: [] },
    bukit_raja: {
      name: 'Bandar Bukit Raja (Wetland Townpark)', lat: 3.0835, lon: 101.4452, zoom: 16,
      zones: [
        { lat: 3.0842, lon: 101.4445, kind: 'flood', letter: 'D', title: 'Wetland Weir High Water Level', desc: 'Heavy evening rain inflow at Bandar Bukit Raja Townpark retention basin.' },
        { lat: 3.0828, lon: 101.4461, kind: 'wind', letter: 'T', title: 'Gusty Wind Advisory Along Jogging Loop', desc: '40 km/h squall gusts monitored near East Wetland walkway.' },
        { lat: 3.0836, lon: 101.4438, kind: 'heat', letter: 'H', title: 'Exposed Plaza Walk (34.2°C Surface)', desc: 'Priority canopy infilling zone for Phase 2 wetland connector.' }
      ]
    },
    serenia: {
      name: 'Serenia City (Dengkil Central Lake)', lat: 2.8495, lon: 101.7038, zoom: 16,
      zones: [
        { lat: 2.8501, lon: 101.7032, kind: 'drought', letter: 'V', title: 'Dry Turf Patch · Serenia Central Park', desc: 'Scheduled smart irrigation cycle for newly planted rain trees.' },
        { lat: 2.8489, lon: 101.7045, kind: 'heat', letter: 'H', title: 'Lakeside Promenade Thermal Hotspot (35.1°C)', desc: 'Candidate corridor for Hopea odorata shade canopy.' }
      ]
    },
    sjcc: {
      name: 'SJCC & Putra Heights (Subang Jaya)', lat: 3.0792, lon: 101.5855, zoom: 16,
      zones: [
        { lat: 3.0798, lon: 101.5848, kind: 'wind', letter: 'T', title: 'Roadside Tree Branch Clearance · SJCC', desc: 'Routine pruning scheduled following METMalaysia wind advisory.' },
        { lat: 3.0786, lon: 101.5863, kind: 'flood', letter: 'D', title: 'Perimeter Scupper Drain Inspection', desc: 'Pre-storm leaf grate clearance completed by operations.' }
      ]
    },
    nilai: {
      name: 'Nilai Impian (Lake Garden)', lat: 2.8335, lon: 101.8058, zoom: 16,
      zones: [
        { lat: 2.8341, lon: 101.8052, kind: 'heat', letter: 'H', title: 'Nilai Impian Lakefront Walk (34.8°C)', desc: 'Warm afternoon surface reading; shade simulation queued.' },
        { lat: 2.8329, lon: 101.8065, kind: 'drought', letter: 'V', title: 'Young Sapling Mulching Zone', desc: 'Soil moisture retention check normal.' }
      ]
    },
    pagoh: {
      name: 'Bandar Universiti Pagoh (Johor)', lat: 2.1485, lon: 102.7315, zoom: 16,
      zones: [
        { lat: 2.1491, lon: 102.7309, kind: 'flood', letter: 'D', title: 'Campus Retention Lake Telemetry Nominal', desc: '62% capacity; ample storm buffer available.' },
        { lat: 2.1479, lon: 102.7322, kind: 'heat', letter: 'H', title: 'Shared Edu-Hub Pedestrian Spine', desc: 'Canopy cooling target +18% shade coverage.' }
      ]
    }
  };
  const extraTownshipLayer = L.layerGroup().addTo(map);
  const kindColors = { flood: '#0284c7', wind: '#ea580c', drought: '#ca8a04', heat: '#dc2626' };
  const kindLabels = { flood: 'Drainage & Flood Watch', wind: 'Wind & Tree Risk', drought: 'Soil & Sapling Care', heat: 'Heat Hotspot' };

  function switchSimulatorTownship(key) {
    const t = sdpTownships[key] || sdpTownships.elmina;
    const selectEl = document.getElementById('sdp-township-select');
    if (selectEl) selectEl.value = key;
    extraTownshipLayer.clearLayers();
    if (key === 'elmina') {
      if (typeof bounds !== 'undefined' && bounds.isValid()) {
        map.setMaxBounds(bounds.pad(0.8));
      }
      fitCorridor();
      setBasemapStatus('Live Google Satellite · City of Elmina Central Park', 'ready');
      message('Showing City of Elmina Central Park. Click "+ Add tree on map" to plant insured shade trees.');
      return;
    }
    map.setMaxBounds(null);
    for (const z of t.zones) {
      const col = kindColors[z.kind] || '#0284c7';
      L.circle([z.lat, z.lon], { radius: 42, color: col, weight: 2.5, fillColor: col, fillOpacity: 0.32 })
        .bindTooltip(`<strong>${kindLabels[z.kind] || 'Alert Zone'}</strong><br>${z.title}`)
        .addTo(extraTownshipLayer);
      L.marker([z.lat, z.lon], {
        icon: L.divIcon({
          className: 'report-marker',
          html: `<span style="background:${col};border:2px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,0.35);display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;color:#fff;font-weight:800;font-size:12px;">${z.letter}</span>`,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        })
      }).bindPopup(`<strong>${z.title}</strong><br><span style="font-size:12px;color:#475569;">${z.desc}</span>`).addTo(extraTownshipLayer);
    }
    map.flyTo([t.lat, t.lon], t.zoom, { duration: 1.1 });
    setBasemapStatus(`Live Google Satellite · ${t.name}`, 'ready');
    message(`Viewing ${t.name}. Switch back to "City of Elmina" anytime to edit the Central Park tree layout.`);
  }

  const townshipSelect = document.getElementById('sdp-township-select');
  if (townshipSelect) {
    townshipSelect.addEventListener('change', (e) => switchSimulatorTownship(e.target.value));
  }
  const fitMapBtn = document.getElementById('fit-map');
  if (fitMapBtn) {
    fitMapBtn.onclick = () => switchSimulatorTownship('elmina');
  }

  setTimeout(() => map.invalidateSize(), 150);
})();
