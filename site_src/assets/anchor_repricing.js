// Live anchor repricing.
//
// Proposed gas is exactly ceil(anchor_rate_gas_per_s * runtime_ms / 1000) — the same
// formula evm-gasfit uses (proposal/aggregate.py). It is strictly linear in the anchor,
// and the worst-case client is anchor-invariant, so we can recompute every cost in the
// browser from the per-row runtime baked into the table. No re-fit, no server.
(function () {
  "use strict";

  var range = document.getElementById("anchor-range");
  var num = document.getElementById("anchor-num");
  var summary = document.getElementById("summary");
  var resultCount = document.getElementById("result-count");
  var onlyIncreases = document.getElementById("only-increases");
  var onlyDecreases = document.getElementById("only-decreases");
  var selects = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var rows = Array.prototype.slice.call(
    document.querySelectorAll("#repricing-table tbody tr")
  );

  function attrFor(name) {
    return "data-" + name;
  }

  function fmt(n) {
    return n.toLocaleString("en-US");
  }

  // Recompute the proposed cost (+ diff/pct/flag) for every row at the given anchor.
  function reprice(mgas) {
    var anchorGasPerS = mgas * 1e6;
    rows.forEach(function (row) {
      var runtimeMs = parseFloat(row.getAttribute("data-runtime"));
      var currentAttr = row.getAttribute("data-current");
      var current = currentAttr === "" ? null : parseInt(currentAttr, 10);
      var proposed = Math.ceil((anchorGasPerS * runtimeMs) / 1000);

      row.querySelector(".proposed").textContent = fmt(proposed);

      var diffCell = row.querySelector(".diff");
      var pctCell = row.querySelector(".pct");
      var flagCell = row.querySelector(".flag");

      if (current === null) {
        // new_params baseline with no prior cost — nothing to diff against.
        diffCell.textContent = "—";
        pctCell.textContent = "—";
        flagCell.textContent = "new";
        diffCell.className = "diff";
        pctCell.className = "pct";
        flagCell.className = "flag";
        row.dataset.needs = "na";
        return;
      }

      var diff = proposed - current;
      var needsIncrease = proposed > current;
      var dir = diff > 0 ? "up" : diff < 0 ? "down" : "";
      diffCell.textContent = (diff > 0 ? "+" : "") + fmt(diff);
      pctCell.textContent =
        current === 0
          ? "—"
          : (diff > 0 ? "+" : "") + Math.round((100 * diff) / current) + "%";
      diffCell.className = "diff " + dir;
      pctCell.className = "pct " + dir;
      flagCell.className = "flag " + dir;
      flagCell.textContent = needsIncrease ? "↑" : diff < 0 ? "↓" : "·";
      row.dataset.needs = needsIncrease ? "1" : "0";
      row.dataset.cheaper = diff < 0 ? "1" : "0";
    });
  }

  // Show/hide rows per the category/client/only-increases filters.
  function applyFilters() {
    rows.forEach(function (row) {
      var visible = selects.every(function (sel) {
        return (
          sel.value === "all" ||
          row.getAttribute(attrFor(sel.dataset.filter)) === sel.value
        );
      });
      if (visible && onlyIncreases.checked) {
        visible = row.dataset.needs === "1";
      }
      if (visible && onlyDecreases.checked) {
        visible = row.dataset.cheaper === "1";
      }
      row.style.display = visible ? "" : "none";
    });
  }

  function updateSummary() {
    var mgas = Number(num.value);
    var shown = 0;
    var priced = 0;
    var needing = 0;
    rows.forEach(function (row) {
      if (row.style.display === "none") return;
      shown++;
      if (row.dataset.needs === "na") return;
      priced++;
      if (row.dataset.needs === "1") needing++;
    });
    summary.innerHTML =
      "<strong>" +
      needing +
      "</strong> of " +
      priced +
      " operations would need a higher gas cost at <strong>" +
      fmt(mgas) +
      "&nbsp;Mgas/s</strong>.";
    if (resultCount) {
      resultCount.textContent = shown + " of " + rows.length + " ops shown";
    }
  }

  function refresh() {
    reprice(Number(num.value));
    applyFilters();
    updateSummary();
  }

  // Keep the slider and the number box in sync (slider clamps to its range; the
  // number box can go beyond it for extreme anchors).
  range.addEventListener("input", function () {
    num.value = range.value;
    refresh();
  });
  num.addEventListener("input", function () {
    var v = Number(num.value);
    if (!isNaN(v)) {
      range.value = Math.min(Math.max(v, range.min), range.max);
    }
    refresh();
  });
  selects.forEach(function (sel) {
    sel.addEventListener("change", function () {
      applyFilters();
      updateSummary();
    });
  });
  [onlyIncreases, onlyDecreases].forEach(function (box) {
    box.addEventListener("change", function () {
      applyFilters();
      updateSummary();
    });
  });

  refresh();
})();
