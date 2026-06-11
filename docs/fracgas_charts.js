// Throughput-loss charts (Plotly, vendored). Reads FRACGAS_ROWS / FRACGAS_SWEEP /
// FRACGAS_HOURLY / ANCHOR_MGAS / HOURLY_MEAN_{ROUND,CURRENT} injected by fracgas.html.
// Every figure compares the three repricing scenarios — no reprice (current gas), reprice +
// round (ceil), reprice + fractional (the zero-loss ideal): two anchor sweeps (opcode-level
// median + gas-weighted traffic), the per-hour traffic-loss distribution, and the per-op loss.
(function () {
  "use strict";
  if (typeof Plotly === "undefined") return;

  // Pick readable colors for light/dark without reading CSS vars (Plotly can't).
  var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  var fg = dark ? "#e6e9ef" : "#1c2430";
  var grid = dark ? "#2a313d" : "#e4e7ec";
  var accent = dark ? "#6ea0ff" : "#2f6fed"; // reprice + round
  var warn = dark ? "#ff9b8e" : "#b42318"; // no reprice
  var ideal = dark ? "#7ee0a0" : "#1a8a4a"; // reprice + fractional (zero)

  var baseLayout = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: fg, family: "-apple-system, Segoe UI, Roboto, sans-serif" },
    margin: { t: 16, r: 16, b: 56, l: 56 },
    xaxis: { gridcolor: grid, zerolinecolor: grid },
    yaxis: { gridcolor: grid, zerolinecolor: grid },
  };
  var config = { responsive: true, displayModeBar: false };

  // Vertical marker + label at the current anchor, shared by both sweep charts.
  function anchorMarker(layout) {
    layout.shapes = (layout.shapes || []).concat([{
      type: "line", x0: ANCHOR_MGAS, x1: ANCHOR_MGAS, yref: "paper", y0: 0, y1: 1,
      line: { color: fg, width: 1, dash: "dash" },
    }]);
    layout.annotations = (layout.annotations || []).concat([{
      x: ANCHOR_MGAS, yref: "paper", y: 1, yanchor: "bottom",
      text: ANCHOR_MGAS + " Mgas/s", showarrow: false, font: { color: fg, size: 11 },
    }]);
    return layout;
  }

  // One anchor-sweep figure: three scenario lines (fractional is a flat zero baseline).
  function sweep(divId, anchors, current, round, yTitle) {
    var zero = anchors.map(function () { return 0; });
    Plotly.newPlot(
      divId,
      [
        {
          x: anchors, y: current, name: "No reprice (current gas)",
          mode: "lines+markers", type: "scatter", line: { color: warn, width: 2.5 },
          connectgaps: true,
          hovertemplate: "%{x} Mgas/s<br>%{y:.2f}% loss<extra>no reprice</extra>",
        },
        {
          x: anchors, y: round, name: "Reprice + round",
          mode: "lines+markers", type: "scatter", line: { color: accent, width: 2.5 },
          hovertemplate: "%{x} Mgas/s<br>%{y:.2f}% loss<extra>round</extra>",
        },
        {
          x: anchors, y: zero, name: "Reprice + fractional (ideal)",
          mode: "lines", type: "scatter", line: { color: ideal, width: 1.5, dash: "dot" },
          hoverinfo: "skip",
        },
      ],
      anchorMarker(Object.assign({}, baseLayout, {
        legend: { orientation: "h", y: -0.28, yanchor: "top", x: 0.5, xanchor: "center" },
        margin: { t: 24, r: 16, b: 92, l: 56 },
        xaxis: Object.assign({}, baseLayout.xaxis, { title: "Anchor (Mgas/s)" }),
        yaxis: Object.assign({}, baseLayout.yaxis, { title: yTitle }),
      })),
      config
    );
  }

  // --- Anchor sweeps -------------------------------------------------------
  if (FRACGAS_SWEEP && FRACGAS_SWEEP.length) {
    var anchors = FRACGAS_SWEEP.map(function (d) { return d.anchor_mgas; });
    var pct = function (key) {
      return FRACGAS_SWEEP.map(function (d) {
        return d[key] == null ? null : d[key] * 100;
      });
    };
    sweep("sweep-opcode-chart", anchors, pct("op_median_current"), pct("op_median_round"),
      "Median per-op loss (%)");
    sweep("sweep-traffic-chart", anchors, pct("traffic_current"), pct("traffic_round"),
      "Traffic loss (%)");
  }

  // --- Per-operation loss --------------------------------------------------
  // Grouped bars: no-reprice overcharge vs rounding overcharge per param (sorted by round).
  if (FRACGAS_ROWS && FRACGAS_ROWS.length) {
    var rows = FRACGAS_ROWS.slice().sort(function (a, b) { return b.rate_round - a.rate_round; });
    var labels = rows.map(function (r) {
      return r.gas_param.replace(/^(OPCODE_|PRECOMPILE_)/, "");
    });
    Plotly.newPlot(
      "perop-chart",
      [
        {
          x: labels,
          y: rows.map(function (r) { return r.rate_current == null ? null : r.rate_current * 100; }),
          name: "No reprice (current gas)", type: "bar", marker: { color: warn },
          hovertemplate: "%{x}<br>%{y:.1f}% loss<extra>no reprice</extra>",
        },
        {
          x: labels,
          y: rows.map(function (r) { return r.rate_round * 100; }),
          name: "Reprice + round", type: "bar", marker: { color: accent },
          customdata: rows.map(function (r) { return r.exact.toFixed(3) + " → " + r.rounded; }),
          hovertemplate: "%{x}<br>%{y:.1f}% loss<br>exact %{customdata} gas<extra>round</extra>",
        },
      ],
      Object.assign({}, baseLayout, {
        barmode: "group",
        height: 500,
        legend: { orientation: "h", y: -0.42, yanchor: "top", x: 0.5, xanchor: "center" },
        margin: { t: 16, r: 16, b: 180, l: 56 },
        xaxis: Object.assign({}, baseLayout.xaxis, { tickangle: -60, tickfont: { size: 9 } }),
        yaxis: Object.assign({}, baseLayout.yaxis, { title: "Loss (% of charged gas)", zeroline: true }),
      }),
      config
    );
  }

  // --- Loss per hour of mainnet traffic ------------------------------------
  // Overlaid distributions of the per-hour gas-weighted loss: no-reprice vs round, each with a
  // dashed mean line. Fractional is 0 (noted in prose, not drawn). We bin in JS to a fixed 0.5%
  // width and draw explicit `bar` traces rather than Plotly `histogram` traces: histogram autobin
  // (even with autobinx:false/xbins) proved unreliable here, picking a bin per distinct value over
  // the ~720 hours and rendering as a jagged comb instead of a distribution. Pre-binning is
  // deterministic — x is the bin center, y the hour count, so it always draws as two clean mounds.
  var HOURLY_BIN = 0.25;
  // Count values into fixed-width bins keyed by bin index; return {x: centers, y: counts} sorted.
  function binCounts(values, size) {
    var counts = {};
    values.forEach(function (v) {
      var k = Math.floor(v / size);
      counts[k] = (counts[k] || 0) + 1;
    });
    var keys = Object.keys(counts).map(Number).sort(function (a, b) { return a - b; });
    return {
      x: keys.map(function (k) { return (k + 0.5) * size; }),
      y: keys.map(function (k) { return counts[k]; }),
    };
  }
  if (FRACGAS_HOURLY && FRACGAS_HOURLY.length) {
    var roundBins = binCounts(FRACGAS_HOURLY.map(function (d) { return d.loss_rate_round * 100; }), HOURLY_BIN);
    var currentBins = binCounts(FRACGAS_HOURLY.map(function (d) { return d.loss_rate_current * 100; }), HOURLY_BIN);
    var shapes = [];
    var annos = [];
    function meanLine(mean, color, label) {
      if (mean == null) return;
      var m = mean * 100;
      shapes.push({
        type: "line", x0: m, x1: m, yref: "paper", y0: 0, y1: 1,
        line: { color: color, width: 1.5, dash: "dash" },
      });
      annos.push({
        x: m, yref: "paper", y: 1, yanchor: "bottom",
        text: label + " " + m.toFixed(1) + "%", showarrow: false, font: { color: color, size: 11 },
      });
    }
    meanLine(HOURLY_MEAN_CURRENT, warn, "no reprice");
    meanLine(HOURLY_MEAN_ROUND, accent, "reprice + round");
    Plotly.newPlot(
      "hourly-chart",
      [
        {
          x: currentBins.x, y: currentBins.y, type: "bar", name: "No reprice (current gas)",
          width: HOURLY_BIN, marker: { color: warn }, opacity: 0.6,
          hovertemplate: "%{y} hours at %{x:.1f}%<extra>no reprice</extra>",
        },
        {
          x: roundBins.x, y: roundBins.y, type: "bar", name: "Reprice + round",
          width: HOURLY_BIN, marker: { color: accent }, opacity: 0.6,
          hovertemplate: "%{y} hours at %{x:.1f}%<extra>round</extra>",
        },
      ],
      Object.assign({}, baseLayout, {
        barmode: "overlay",
        bargap: 0.04,
        legend: { orientation: "h", y: -0.28, yanchor: "top", x: 0.5, xanchor: "center" },
        margin: { t: 24, r: 16, b: 92, l: 56 },
        shapes: shapes,
        annotations: annos,
        xaxis: Object.assign({}, baseLayout.xaxis, { title: "Hourly traffic loss (%)", rangemode: "tozero" }),
        yaxis: Object.assign({}, baseLayout.yaxis, { title: "Number of hours", rangemode: "tozero" }),
      }),
      config
    );
  }
})();
