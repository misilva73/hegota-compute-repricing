// Reference table: category filter + click-to-sort. Same vanilla style as
// bottleneck_filter.js, minus the bottleneck-only checkbox.
(function () {
  "use strict";

  var table = document.getElementById("reference-table");
  if (!table) return;
  var tbody = table.querySelector("tbody");
  var rows = Array.prototype.slice.call(tbody.querySelectorAll("tr"));
  var selects = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var resultCount = document.getElementById("result-count");

  function applyFilters() {
    rows.forEach(function (row) {
      var visible = selects.every(function (sel) {
        return sel.value === "all" ||
               row.getAttribute("data-" + sel.dataset.filter) === sel.value;
      });
      row.style.display = visible ? "" : "none";
    });
    if (resultCount) {
      var shown = rows.filter(function (r) { return r.style.display !== "none"; }).length;
      resultCount.textContent = shown + " of " + rows.length + " operations shown";
    }
  }

  var sortState = {};
  function sortBy(key) {
    var dir = (sortState[key] = -(sortState[key] || -1));
    rows.sort(function (a, b) {
      return a.getAttribute("data-" + key).localeCompare(b.getAttribute("data-" + key)) * dir;
    });
    rows.forEach(function (r) { tbody.appendChild(r); });
  }

  table.querySelectorAll("th[data-sort]").forEach(function (th) {
    th.style.cursor = "pointer";
    th.addEventListener("click", function () { sortBy(th.dataset.sort); });
  });
  selects.forEach(function (sel) { sel.addEventListener("change", applyFilters); });
  applyFilters();
})();
