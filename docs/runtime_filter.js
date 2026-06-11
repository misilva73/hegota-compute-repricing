// Client-side hide/show for the runtime and glue pages.
//
// Each fit block is a <section class="fit-section" data-opcode="…" data-client="…">
// (the glue page uses data-glue-opcode in place of data-opcode). Two <select>
// controls filter the visible sections; "all" matches everything. The control
// markup sets data-filter to the section attribute it drives, so this script is
// shared verbatim between both pages.
(function () {
  "use strict";

  var selects = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  if (selects.length === 0) return;

  var sections = Array.prototype.slice.call(document.querySelectorAll(".fit-section"));

  function attrFor(filterKey) {
    // data-filter="opcode" → section attribute "data-opcode"
    return "data-" + filterKey;
  }

  function apply() {
    sections.forEach(function (section) {
      var visible = selects.every(function (sel) {
        var want = sel.value;
        if (want === "all") return true;
        return section.getAttribute(attrFor(sel.dataset.filter)) === want;
      });
      section.style.display = visible ? "" : "none";
    });
    updateCount();
  }

  function updateCount() {
    var counter = document.getElementById("result-count");
    if (!counter) return;
    var shown = sections.filter(function (s) { return s.style.display !== "none"; }).length;
    counter.textContent = shown + " of " + sections.length + " fits shown";
  }

  selects.forEach(function (sel) { sel.addEventListener("change", apply); });
  apply();
})();
