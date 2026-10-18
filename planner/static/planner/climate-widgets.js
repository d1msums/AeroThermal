(() => {
  "use strict";

  const root = document.getElementById("at-climate");
  if (!root) return;

  const el = id => root.querySelector(`#${id}`);

  const text = (id, value) => {
    el(id).textContent = value;
  };

  const volume = n => `${n.toLocaleString("en-MY")} m³`;

  // DEMONSTRATION ASSUMPTIONS.
  // These are not verified Elmina operating specifications.
  const totalStorageM3 = 100000;
  const targetBeforeStormM3 = 55000;
  const minimumReserveM3 = 30000;

  const scenarios = {
    normal: {
      stored: 65000,
      condition: "Normal",
      score: 92,
      cooling: -2.5
    },

    storm: {
      stored: 65000,
      condition: "Normal · storm watch",
      score: 92,
      cooling: -2.5
    },

    heat: {
      stored: 65000,
      condition: "Heatwave scenario",
      score: 92,
      cooling: -2.5
    },

    drought: {
      stored: 25000,
      condition: "Low storage · dry land",
      score: null,
      cooling: null
    }
  };

  function render() {
    const mode = el("at-scenario").value;
    const s = scenarios[mode];

    const capacity = Math.round(
      s.stored / totalStorageM3 * 100
    );

    const buffer = totalStorageM3 - s.stored;

    // Widget 1: storage and available space.
    text("at-capacity", `${capacity}% Capacity`);
    text("at-condition", s.condition);

    el("at-storage").value = capacity;

    text("at-buffer", volume(buffer));
    text("at-stored", volume(s.stored));

    text(
      "at-water-note",
      mode === "drought"
        ? "Drought / El Niño demo: conserve water; dry-land stress needs review."
        : mode === "heat"
          ? "Heatwave demo: review shaded routes and urban heat hotspots."
          : "Demonstration storage balance; no live water-level sensor."
    );

    // Widget 2: scenario advisory.
    el("at-alert").dataset.tone = mode;
    text("at-release", "");

    if (mode === "storm") {
      const candidate = Math.max(
        0,
        Math.min(
          s.stored - targetBeforeStormM3,
          s.stored - minimumReserveM3
        )
      );

      text(
        "at-alert-state",
        "SIMULATED WARNING · Not issued by METMalaysia"
      );

      text(
        "at-alert-title",
        "Heavy Rainfall Warning · next 12h"
      );

      text(
        "at-alert-message",
        `Recommend operator review of pre-discharging ${volume(candidate)} ` +
        "to the main river to create extra storage before the storm. " +
        "Downstream conditions and permitted release rate are not assessed."
      );

      text(
        "at-release",
        `If approved and completed: ${volume(buffer + candidate)} buffer ` +
        "before new inflow (illustrative)."
      );

    } else if (mode === "drought") {
      text(
        "at-alert-state",
        "DEMO · Water conservation"
      );

      text(
        "at-alert-title",
        "Pre-discharge held for review"
      );

      text(
        "at-alert-message",
        "Stored water is below the assumed 30,000 m³ reserve. " +
        "No pre-discharge is proposed in this drought scenario."
      );

    } else if (mode === "heat") {
      text(
        "at-alert-state",
        "DEMO · Extreme heat / heat islands"
      );

      text(
        "at-alert-title",
        "Review cooling and water retention"
      );

      text(
        "at-alert-message",
        "Use the existing tree-shade simulator to compare shade. " +
        "Heat-island intensity and air-temperature reduction are not measured here."
      );

    } else {
      text(
        "at-alert-state",
        "DEMO · Normal conditions"
      );

      text(
        "at-alert-title",
        "No storm selected in this demo"
      );

      text(
        "at-alert-message",
        "Choose Heavy rain to demonstrate the advisory. " +
        "This is not an all-clear from a live weather service."
      );
    }

    // Indicator: display the two sample metrics separately.
    const hasScore = Number.isFinite(s.score);

    text(
      "at-flood",
      hasScore ? `${s.score}%` : "N/A"
    );

    el("at-gauge").style.setProperty(
      "--at-score",
      `${hasScore ? s.score : 0}%`
    );

    text(
      "at-cooling",
      Number.isFinite(s.cooling)
        ? `${s.cooling.toFixed(1)}°C`
        : "N/A"
    );
  }

  el("at-scenario").addEventListener("change", render);

  render();
})();