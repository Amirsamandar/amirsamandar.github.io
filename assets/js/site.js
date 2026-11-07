/* Theme toggle. Without JavaScript the site follows the system color scheme and
   the button stays hidden. The choice is stored per browser when storage works. */
(function () {
  "use strict";
  var root = document.documentElement;
  var button = document.querySelector(".theme-toggle");
  if (!button) { return; }
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function current() {
    var t = root.getAttribute("data-theme");
    if (t === "light" || t === "dark") { return t; }
    return media && media.matches ? "dark" : "light";
  }
  function sync() {
    var isDark = current() === "dark";
    button.setAttribute("aria-pressed", isDark ? "true" : "false");
    button.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
    button.querySelector(".theme-toggle__label").textContent = isDark ? "Light" : "Dark";
  }
  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { window.localStorage.setItem("theme", next); } catch (e) {}
    sync();
  });
  if (media && media.addEventListener) { media.addEventListener("change", sync); }
  button.hidden = false;
  sync();
})();
