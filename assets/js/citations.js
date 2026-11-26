/* Filters for the Citations page. Without JavaScript every citing paper is
   listed and the filter form stays hidden. Filter state is kept in the URL
   (?paper=...&source=...&noself=1&q=...) so a filtered view can be linked. */
(function () {
  "use strict";
  var form = document.getElementById("cite-filters");
  var list = document.getElementById("citing-list");
  if (!form || !list) { return; }
  var items = Array.prototype.slice.call(list.children);
  var paper = document.getElementById("cf-paper");
  var source = document.getElementById("cf-source");
  var noself = document.getElementById("cf-noself");
  var query = document.getElementById("cf-q");
  var count = document.getElementById("cf-count");

  function norm(s) {
    s = (s || "").toLowerCase();
    return s.normalize ? s.normalize("NFD").replace(/[̀-ͯ]/g, "") : s;
  }
  function words(s) { return s ? s.split(" ") : []; }

  function apply(push) {
    var p = paper.value, src = source.value, ns = noself.checked;
    var q = norm(query.value).trim().split(/\s+/).filter(Boolean);
    var shown = 0;
    items.forEach(function (li) {
      var cites = words(li.getAttribute("data-cites"));
      var self = words(li.getAttribute("data-self"));
      var ok;
      if (p) {
        ok = cites.indexOf(p) >= 0 && (!ns || self.indexOf(p) < 0);
      } else {
        ok = !ns || cites.some(function (c) { return self.indexOf(c) < 0; });
      }
      if (ok && src) { ok = words(li.getAttribute("data-sources")).indexOf(src) >= 0; }
      if (ok && q.length) {
        var hay = li.getAttribute("data-search") || "";
        ok = q.every(function (w) { return hay.indexOf(w) >= 0; });
      }
      li.hidden = !ok;
      if (ok) { shown++; }
    });
    var label = paper.selectedIndex > 0 ? " citing " + paper.options[paper.selectedIndex].text.replace(/\s*\(\d+\)$/, "") : "";
    count.textContent = shown === items.length
      ? items.length + " citing papers, newest first."
      : "Showing " + shown + " of " + items.length + " citing papers" + label + ".";
    if (push && window.history && history.replaceState) {
      var params = new URLSearchParams();
      if (p) { params.set("paper", p); }
      if (src) { params.set("source", src); }
      if (ns) { params.set("noself", "1"); }
      if (query.value.trim()) { params.set("q", query.value.trim()); }
      var qs = params.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
    }
  }

  var params = new URLSearchParams(location.search);
  function setSelect(el, v) {
    if (v && Array.prototype.some.call(el.options, function (o) { return o.value === v; })) { el.value = v; }
  }
  setSelect(paper, params.get("paper"));
  setSelect(source, params.get("source"));
  noself.checked = params.get("noself") === "1";
  query.value = params.get("q") || "";

  [paper, source, noself].forEach(function (el) { el.addEventListener("change", function () { apply(true); }); });
  query.addEventListener("input", function () { apply(true); });
  form.hidden = false;
  apply(false);
})();
