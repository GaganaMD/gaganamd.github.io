/* Small progressive enhancements. Every page works without JavaScript. */
(function () {
  // Old single-page anchors -> new pages, so existing links keep working.
  var moved = { '#projects': 'projects.html', '#writing': 'writing.html', '#experience': 'about.html#experience', '#about': 'about.html', '#home': 'index.html' };
  var path = location.pathname;
  if ((path === '/' || /index\.html$/.test(path)) && moved[location.hash]) {
    location.replace(moved[location.hash]);
    return;
  }

  // Mobile navigation
  var menu = document.getElementById('menu');
  var nav = document.getElementById('nav-links');
  if (menu && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('open', open);
      menu.setAttribute('aria-expanded', String(open));
      menu.textContent = open ? 'Close' : 'Menu';
    };
    menu.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); menu.focus(); }
    });
  }

  // Project filters (projects page only)
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.filter'));
  var items = Array.prototype.slice.call(document.querySelectorAll('.archive-item'));
  var count = document.getElementById('project-count');
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var cat = b.getAttribute('data-category');
      var n = 0;
      buttons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      items.forEach(function (x) {
        var show = cat === 'all' || x.getAttribute('data-category') === cat;
        x.hidden = !show;
        if (show) n++;
      });
      if (count) count.textContent = cat === 'all' ? 'Showing all projects' : 'Showing ' + n + ' of ' + items.length + ' projects: ' + b.textContent;
    });
  });

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
