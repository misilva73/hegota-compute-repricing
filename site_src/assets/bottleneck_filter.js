// Bottleneck table: live throughput anchor, category filter, "only bottlenecks"
// toggle, click-to-sort.
//
// The worst-case Mgas/s per op is a measured throughput — anchor-invariant — so moving
// the anchor only re-decides which ops fall below it. We recompute the bottleneck flag,
// the highlight, and the counts in the browser; no re-fit, no server. Same vanilla,
// dependency-free style as anchor_repricing.js.
(function () {
  "use strict";

  var table = document.getElementById("bottleneck-table");
  if (!table) return;
  var tbody = table.querySelector("tbody");
  var rows = Array.prototype.slice.call(tbody.querySelectorAll("tr"));
  var selects = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var onlyBelow = document.getElementById("only-below");
  var resultCount = document.getElementById("result-count");
  var range = document.getElementById("anchor-range");
  var num = document.getElementById("anchor-num");
  var summary = document.getElementById("summary");
  var anchorLabel = document.getElementById("anchor-label");

  function fmt(n) {
    return n.toLocaleString("en-US");
  }

  // Re-decide each op's bottleneck status against the current anchor and repaint the
  // worst-case highlight + flag. Each per-client cell is also highlighted when that
  // client runs the op below the anchor. data-below is kept in sync for the filter.
  function reanchor(mgas) {
    rows.forEach(function (row) {
      var worst = parseFloat(row.getAttribute("data-worst"));
      var below = !isNaN(worst) && worst < mgas;
      row.dataset.below = below ? "1" : "0";
      var worstCell = row.querySelector(".worst");
      if (worstCell) worstCell.classList.toggle("worst-case", below);
      var flagCell = row.querySelector(".flag");
      if (flagCell) flagCell.innerHTML = below ? "⚠" : "";
      Array.prototype.forEach.call(
        row.querySelectorAll(".client-cell"),
        function (cell) {
          var v = parseFloat(cell.getAttribute("data-mgas"));
          cell.classList.toggle("worst-case", !isNaN(v) && v < mgas);
        }
      );
    });
    if (anchorLabel) anchorLabel.textContent = fmt(mgas);
  }

  function applyFilters() {
    rows.forEach(function (row) {
      var visible = selects.every(function (sel) {
        return (
          sel.value === "all" ||
          row.getAttribute("data-" + sel.dataset.filter) === sel.value
        );
      });
      if (visible && onlyBelow.checked) visible = row.dataset.below === "1";
      row.style.display = visible ? "" : "none";
    });
    if (resultCount) {
      var shown = rows.filter(function (r) { return r.style.display !== "none"; }).length;
      resultCount.textContent = shown + " of " + rows.length + " ops shown";
    }
  }

  function updateSummary() {
    var mgas = Number(num.value);
    var nBelow = rows.filter(function (r) { return r.dataset.below === "1"; }).length;
    if (!summary) return;
    summary.innerHTML =
      "<strong>" + nBelow + "</strong> of " + rows.length +
      " compute operations fall below <strong>" + fmt(mgas) + "&nbsp;Mgas/s</strong>." +
      (nBelow === 0
        ? " Every compute operation clears the ceiling — the genuine sub-anchor ops are" +
          " all state/IO (storage, calls, transfers), which are out of scope here."
        : "");
  }

  // Click a header to sort by that column; click again to reverse.
  var sortState = {};
  function sortBy(key, numeric) {
    var dir = (sortState[key] = -(sortState[key] || -1));
    rows.sort(function (a, b) {
      var av = a.getAttribute("data-" + key);
      var bv = b.getAttribute("data-" + key);
      if (numeric) {
        av = parseFloat(av);
        bv = parseFloat(bv);
        if (isNaN(av)) av = Infinity;
        if (isNaN(bv)) bv = Infinity;
        return (av - bv) * dir;
      }
      return av.localeCompare(bv) * dir;
    });
    rows.forEach(function (r) { tbody.appendChild(r); });
  }

  function refresh() {
    reanchor(Number(num.value));
    applyFilters();
    updateSummary();
  }

  table.querySelectorAll("th[data-sort]").forEach(function (th) {
    th.style.cursor = "pointer";
    th.addEventListener("click", function () {
      sortBy(th.dataset.sort, th.dataset.num === "1");
    });
  });
  selects.forEach(function (sel) { sel.addEventListener("change", applyFilters); });
  onlyBelow.addEventListener("change", applyFilters);

  // Keep slider and number box in sync (slider clamps to its range; the number box can
  // go beyond it for extreme anchors).
  if (range && num) {
    range.addEventListener("input", function () {
      num.value = range.value;
      refresh();
    });
    num.addEventListener("input", function () {
      var v = Number(num.value);
      if (!isNaN(v)) range.value = Math.min(Math.max(v, range.min), range.max);
      refresh();
    });
  }

  refresh();
})();
