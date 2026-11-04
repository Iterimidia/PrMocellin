/*
  Black Friday: configuração central (vale para a home e as 5 páginas de curso).
  A promoção só aparece entre "inicio" e "fim" E com todos os links preenchidos.
  Fora disso, o site mostra os preços e links oficiais.
  Prévia: abra qualquer página com ?bf=1 (desligar a prévia: ?bf=0).
*/
(function(){
  var BF = {
    inicio: null,                         // null = já começou
    fim: "2026-11-30T23:59:59-03:00",     // 30/11 às 23:59 (horário de Brasília)
    links: {
      sexualidadecrista: "https://sun.eduzz.com/2194009",
      homeschooling: "https://sun.eduzz.com/1686279",
      criacaodefilhos: "https://sun.eduzz.com/1704004",
      culpadomeucorpo: "https://sun.eduzz.com/1702808",
      mentecrista: "https://sun.eduzz.com/7WX5YANO0A"
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

  // Só na prévia sem data definida: contador de demonstração (3 dias)
  if (preview && !fim) fim = Date.now() + 3 * 86400000;

  document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('[data-bf-link]').forEach(function(a){
      var url = BF.links[a.getAttribute('data-bf-link')];
      if (url) a.href = url;
    });

    // A faixa do topo fica fixa; o menu fica logo abaixo dela
    var bar = document.querySelector('.bfbar');
    function medir(){ if (bar) root.style.setProperty('--bfh', bar.offsetHeight + 'px'); }
    medir();
    window.addEventListener('resize', medir);

    var timers = document.querySelectorAll('.bf-timer');
    if (!fim || fim <= Date.now()) {
      timers.forEach(function(t){ t.style.display = 'none'; });
      medir();
      return;
    }
    function pad(n){ return n < 10 ? '0' + n : '' + n; }
    function tick(){
      var s = Math.max(0, Math.floor((fim - Date.now()) / 1000));
      if (s === 0 && !preview) { location.reload(); return; }
      var v = { d: pad(Math.floor(s / 86400)), h: pad(Math.floor(s % 86400 / 3600)),
                m: pad(Math.floor(s % 3600 / 60)), s: pad(s % 60) };
      timers.forEach(function(t){
        t.querySelectorAll('[data-u]').forEach(function(el){ el.textContent = v[el.getAttribute('data-u')]; });
      });
    }
    tick();
    setInterval(tick, 1000);
  });
})();
