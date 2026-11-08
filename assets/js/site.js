/* Theme toggle. The site is dark by default; the toggle switches to light.
   Without JavaScript the site stays dark and the button stays hidden.
   The choice is stored per browser when storage works. */
(function () {
  "use strict";
  var root = document.documentElement;
  var button = document.querySelector(".theme-toggle");
  if (!button) { return; }
  function current() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
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
  button.hidden = false;
  sync();
})();
