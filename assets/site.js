// Comportamentos compartilhados: menu do celular e entrada suave das seções
(function(){
  var btn = document.getElementById('menuBtn'), nav = document.getElementById('nav');
  if (btn && nav) {
    function fechar(){ nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    btn.addEventListener('click', function(ev){
      ev.stopPropagation();
      var aberto = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', aberto ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', fechar); });
    document.addEventListener('keydown', function(ev){ if (ev.key === 'Escape') fechar(); });
    document.addEventListener('click', function(ev){ if (nav.classList.contains('open') && !nav.contains(ev.target)) fechar(); });
  }
  if ('IntersectionObserver' in window) {
    document.documentElement.classList.add('js');
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.fade').forEach(function(el){ io.observe(el); });
    setTimeout(function(){ document.querySelectorAll('.fade').forEach(function(el){ el.classList.add('in'); }); }, 3000);
  }
})();
