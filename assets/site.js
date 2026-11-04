// Comportamentos compartilhados: menu do celular e entrada suave das seções
(function(){
  var btn = document.getElementById('menuBtn'), nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function(){ var o = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o); });
    nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ nav.classList.remove('open'); btn.setAttribute('aria-expanded', false); }); });
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
