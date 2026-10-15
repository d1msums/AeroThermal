/* Extension for EcoCool concept-v2 dashboard; GoogleMutant 0.16.0 + Leaflet 1.9.4. */
(() => {
  'use strict';
  if (typeof site === 'undefined' || site.basemap?.provider !== 'google') return;
  const setText = (selector, text) => {
    const node = document.querySelector(selector);
    if (node) node.textContent = text;
  };
  setText('.concept-badge', site.data_label);
  setText('.map-meta', ' / Elmina map pilot');
  setText('.map-note', 'OSM PILOT · HYPOTHETICAL PLANTING');
  setText('.method', site.method_note);
  setText('.legend span:first-child', 'Existing trees: not inventoried');
  setText('#run', 'Calculate proposed-tree shade →');
  setText('.cards article:nth-child(1) > span', 'Existing shade (not surveyed)');
  setText('.cards article:nth-child(1) > small', 'No complete tree inventory');
  setText('.cards article:nth-child(2) > span', 'Shade from proposed trees');
  setText('.cards article:nth-child(2) > small', 'Selected route centreline only');
  setText('.cards article:nth-child(3) > span', 'Improvement vs existing');
  setText('#shadow-mode option[value="baseline"]', 'Existing: not inventoried');
  setText('#shadow-mode option[value="proposed"]', 'Proposed-tree shade');
  map.setMinZoom(14);
  map.options.zoomSnap = 1;
  map.options.zoomDelta = 1;
  landscape.setStyle(feature => {
    const styles = {
      pilot_boundary: {color:'#ffffff', weight:2, dashArray:'7 5', fillOpacity:0},
      pilot_water: {color:'#70d9f1', weight:2, fillColor:'#27a8ce', fillOpacity:0.10},
      context_path: {color:'#ffffff', weight:2, opacity:0.7},
      evaluated_route: {color:'#ffdc63', weight:5, opacity:1}
    };
    return {...styles[feature.properties.kind], interactive:false};
  });
  shadowLayer.options.style = {color:'#e5b9ff', weight:1.5, fillColor:'#b97cf0', fillOpacity:0.5};
  map.attributionControl.removeAttribution('EcoCool illustrative geometry');
  map.attributionControl.addAttribution('Geometry © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>');
  const routeSwatch = document.querySelector('.swatch.route');
  if (routeSwatch) routeSwatch.style.background = '#ffdc63';
  fit();
  // An empty inventory must never be presented as a measured zero baseline.
  const originalClearMetrics = clearMetrics;
  clearMetrics = function () {
    originalClearMetrics();
    if (site.baseline_inventory_available === false) {
      $('baseline-value').textContent = 'Not surveyed';
      $('baseline-value').style.fontSize = '21px';
      $('delta-value').textContent = 'Unknown';
      $('delta-value').style.fontSize = '24px';
      $('seat-value').textContent = 'Seat inventory unavailable';
    }
  };
  const originalPresent = present;
  present = function (result) {
    originalPresent(result);
    if (site.baseline_inventory_available === false) {
      $('baseline-value').textContent = 'Not surveyed';
      $('baseline-bar').style.width = '0%';
      $('delta-value').textContent = 'Unknown';
      $('seat-value').textContent = 'Seat inventory unavailable';
      if (result.mode === 'simulation') {
        message(`Proposed-tree shade calculated. ${site.method_note} ${(result.warnings || []).join(' ')}`);
      }
    }
  };
  clearMetrics();
  if (!proposedTrees.length) message('Elmina pilot ready. Load an example or place trees, then calculate their projected shade.');
  const status = document.createElement('div');
  status.id = 'basemap-status';
  status.setAttribute('role', 'status');
  status.style.cssText = 'padding:10px 16px;background:#edf2e8;color:#284336;font-size:12px;border-bottom:1px solid #d5dfcd';
  document.querySelector('.map-toolbar').before(status);
  const configNode = document.getElementById('ecocool-map-config');
  let config = {};
  try { config = JSON.parse(configNode?.textContent || '{}'); } catch (_) {}
  const key = (config.google_maps_api_key || '').trim();
  if (!key) {
    status.textContent = 'Google key missing: showing vector reference only. Set GOOGLE_MAPS_API_KEY and restart Django.';
    return;
  }
  let googleLayer = null, loaded = false, failed = false;
  function fail(text) {
    failed = true;
    if (googleLayer) map.removeLayer(googleLayer);
    status.textContent = text + ' Vector reference remains available.';
  }
  window.gm_authFailure = () => fail('Google rejected the key. Check API access and allowed websites in Google Cloud.');
  window.ecocoolGoogleMapsReady = () => {
    if (failed) return;
    try {
      googleLayer = L.gridLayer.googleMutant({type:'satellite', maxZoom:21});
      googleLayer.on('load', () => {
        if (failed) return;
        loaded = true;
        status.textContent = 'Google satellite background · OSM reference geometry · tree proposals are hypothetical';
      });
      googleLayer.addTo(map);
    } catch (error) {
      fail('Google map could not initialise. Check the browser console.');
    }
  };
  status.textContent = 'Loading Google satellite background…';
  const script = document.createElement('script');
  const params = new URLSearchParams({key, callback:'ecocoolGoogleMapsReady', loading:'async', v:'weekly'});
  script.src = 'https://maps.googleapis.com/maps/api/js?' + params.toString();
  script.async = true;
  script.onerror = () => fail('Google could not be reached. Check internet access or browser blocking.');
  document.head.append(script);
  setTimeout(() => {
    if (!loaded && !failed) status.textContent = 'Satellite loading is not confirmed. Check internet access, Google key restrictions and the browser console.';
  }, 15000);
})();
