/*
  Black Friday — configuração central (vale para a home e as 5 páginas de curso).
  A promoção só aparece entre "inicio" e "fim" E com todos os links preenchidos.
  Fora disso, o site mostra os preços e links oficiais.
  Prévia: abra qualquer página com ?bf=1 (desligar a prévia: ?bf=0).
*/
(function(){
  var BF = {
    inicio: null, // ex.: "2026-11-27T00:00:00-03:00"
    fim: null,    // ex.: "2026-11-30T23:59:59-03:00"
    links: {
      sexualidadecrista: "",
      homeschooling: "",
      criacaodefilhos: "",
      culpadomeucorpo: "",
      mentecrista: ""
    }
  };

  var root = document.documentElement;
  var now = Date.now();
  var inicio = BF.inicio ? Date.parse(BF.inicio) : null;
  var fim = BF.fim ? Date.parse(BF.fim) : null;

  var preview = false;
  try {
    var q = new URLSearchParams(location.search).get('bf');
    if (q === '1') sessionStorage.setItem('bf-preview', '1');
    if (q === '0') sessionStorage.removeItem('bf-preview');
    preview = sessionStorage.getItem('bf-preview') === '1';
  } catch (e) {}

  var linksOk = Object.keys(BF.links).every(function(k){ return !!BF.links[k]; });
  var noPeriodo = fim !== null && now < fim && (inicio === null || now >= inicio);
  var ativo = (noPeriodo && linksOk) || preview;
  if (!ativo) return;

  root.classList.add('bf');

  document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('[data-bf-link]').forEach(function(a){
      var url = BF.links[a.getAttribute('data-bf-link')];
      if (url) a.href = url;
    });

    var timers = document.querySelectorAll('.bf-timer');
    if (!fim || fim <= Date.now()) {
      timers.forEach(function(t){ t.style.display = 'none'; });
      return;
    }
    function pad(n){ return n < 10 ? '0' + n : '' + n; }
    function tick(){
      var s = Math.max(0, Math.floor((fim - Date.now()) / 1000));
      if (s === 0 && !preview) { location.reload(); return; }
      var d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600),
          m = Math.floor(s % 3600 / 60), sec = s % 60;
      var txt = (d ? d + 'd ' : '') + pad(h) + 'h ' + pad(m) + 'm ' + pad(sec) + 's';
      timers.forEach(function(t){ t.querySelector('b').textContent = txt; });
    }
    tick();
    setInterval(tick, 1000);
  });
})();
