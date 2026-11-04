"""Gera as 5 páginas de curso (/<slug>/index.html) a partir de ferramentas/cursos.json.

Uso (na raiz do repositório):  python3 ferramentas/gerar_cursos.py
Textos de cada curso: edite cursos.json. Preços e cores: edite CONFIG abaixo.
Links promocionais e datas da Black Friday: black-friday.js.
"""
import json, os
from html import escape as e

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://prmocellin.netlify.app"

CONFIG = {
    # slug: (cor escura, cor de destaque, cor do texto sobre o destaque, foto, preço oficial, preço Black Friday, público)
    "criacaodefilhos":   ("#3B0D72", "#F5811E", "#14120E", "curso-criacao",       250, 165, "Para pais"),
    "homeschooling":     ("#0F3274", "#E23B34", "#FFFFFF", "curso-homeschooling", 250, 165, "Para quem quer educar em casa"),
    "sexualidadecrista": ("#231A0B", "#C8A03C", "#14120E", "curso-sexualidade",   149, 100, "Para casais e jovens"),
    "culpadomeucorpo":   ("#0B2C44", "#2E9AC8", "#14120E", "curso-culpa",         249, 165, "Para quem luta com a própria imagem"),
    "mentecrista":       ("#0F3B31", "#4FD1A0", "#14120E", "curso-mente",         399, 165, "Para quem quer pensar biblicamente"),
}
NOMES = {"criacaodefilhos": "Criação de Filhos", "homeschooling": "Homeschooling", "sexualidadecrista": "Sexualidade Cristã",
         "culpadomeucorpo": "A Culpa é do Meu Corpo", "mentecrista": "Mente Cristã"}

SETA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>'
CADEADO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'
FEATS = [('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9l5 3-5 3V9z"/></svg>', "Videoaulas"),
         ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h13v14H6a2 2 0 0 1-2-2V5zM17 7h3v12H6"/></svg>', "Material complementar"),
         ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="9" r="6"/><path d="M8 14l-1 7 5-3 5 3-1-7"/></svg>', "Certificado"),
         ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>', "Acesso por 12 meses")]


def cd(curto=False):
    if curto:
        return ('<span class="cd"><span><b data-u="d">00</b><i>d</i></span><span><b data-u="h">00</b><i>h</i></span>'
                '<span><b data-u="m">00</b><i>m</i></span><span><b data-u="s">00</b><i>s</i></span></span>')
    return ('<div class="cd"><span><b data-u="d">00</b><i>dias</i></span><span><b data-u="h">00</b><i>horas</i></span>'
            '<span><b data-u="m">00</b><i>min</i></span><span><b data-u="s">00</b><i>seg</i></span></div>')


def dados_estruturados(slug, d):
    """Schema.org (JSON-LD) para Google e IAs: curso, perguntas frequentes e trilha de navegação."""
    c, accent, accent_ink, foto, oficial, promo, publico = CONFIG[slug]
    url = f"{SITE}/{slug}/"
    pastor = {"@type": "Person", "@id": f"{SITE}/#pastor", "name": "Rodrigo Mocellin", "url": f"{SITE}/"}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Course", "@id": url + "#curso", "name": d["name"], "description": d["description"], "url": url,
         "inLanguage": "pt-BR", "image": f"{SITE}/assets/img/{foto}.jpg", "provider": pastor,
         "audience": {"@type": "Audience", "audienceType": publico},
         "teaches": [t for t, _ in d["about_feats"]],
         "syllabusSections": [{"@type": "Syllabus", "name": t, "description": p} for t, p in d["mods"]],
         "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online", "instructor": pastor},
         "offers": {"@type": "Offer", "category": "Paid", "price": f"{oficial}.00", "priceCurrency": "BRL",
                    "url": url + "#inscrever", "availability": "https://schema.org/InStock"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                             for q, a in d["faq"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": d["name"], "item": url}]},
    ]}
    return json.dumps(ld, ensure_ascii=False, indent=1).replace("</", "<\\/")


def pagina(slug, d):
    c, accent, accent_ink, foto, oficial, promo, publico = CONFIG[slug]
    pct = int((oficial - promo) * 100 / oficial)
    nome = d["name"]
    link = e(d["link"])
    comprar = lambda txt, cls="btn btn-accent": f'<a data-bf-link="{slug}" href="{link}" target="_blank" rel="noopener" class="{cls}">{txt} {SETA}</a>'
    quote = ""
    if d.get("quote"):
        quote = f'<div class="lp-quote"><p>“{e(d["quote"][0])}”</p><cite>{e(d["quote"][1])}</cite></div>'
    pontos = "".join(f'<div class="point"><i>{i:02d}</i><div><b>{e(b)}</b><span>{e(s)}</span></div></div>'
                     for i, (b, s) in enumerate(d["about_feats"], 1))
    mods = "".join(f'<div class="mod fade"><i>{i:02d}</i><h3>{e(t)}</h3><p>{e(p)}</p></div>'
                   for i, (t, p) in enumerate(d["mods"], 1))
    facts = "".join(f'<div><b>{e(b)}</b><span>{e(s)}</span></div>' for b, s in d["prof_facts"])
    profp = "".join(f'<p>{e(p)}</p>' for p in d["prof_ps"])
    depos = "".join(f'<div class="depo fade"><div class="stars">★★★★★</div><p>{e(p)}</p><cite>{e(ci)}</cite></div>'
                    for p, ci in d["depos"])
    incl = "".join(f'<div>{CHECK}<span>{e(x)}</span></div>' for x in d["invest_list"])
    faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    feats = "".join(f'<span>{svg}{t}</span>' for svg, t in FEATS)
    outros = "".join(f'<a href="/{s}/">{n}</a>' for s, n in NOMES.items() if s != slug)
    x_oficial = e(d["price_x"])
    titulo = e(d["title"])
    desc = e(d["description"])

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{slug}/">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Pr. Rodrigo Mocellin">
<meta name="theme-color" content="{c}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" as="image" href="/assets/img/{foto}.jpg" fetchpriority="high">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Pr. Rodrigo Mocellin">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{slug}/">
<meta property="og:image" content="{SITE}/assets/img/{foto}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/curso.css">
<style>:root{{--c:{c};--accent:{accent};--accent-ink:{accent_ink}}}</style>
<script src="/black-friday.js"></script>
<script type="application/ld+json">
{dados_estruturados(slug, d)}
</script>
</head>
<body>
<a class="skip" href="#inicio">Pular para o conteúdo</a>

<div class="bfbar bf-only" role="region" aria-label="Black Friday">
  <div class="wrap">
    <strong>Black Friday</strong>
    <span class="t2">{e(nome)} de R$ {oficial} por R$ {promo}</span>
    <span class="bf-timer"><span class="l">Termina em</span>{cd(True)}</span>
    <a href="#inscrever">Aproveitar</a>
  </div>
</div>

<header class="site-header">
  <div class="wrap nav">
    <a href="#inicio" class="brand"><img src="/assets/img/{slug}-logo.png" alt="{e(nome)}"></a>
    <nav class="nav-links" id="nav" aria-label="Menu principal">
      <a href="#curso">O curso</a>
      <a href="#conteudo">Conteúdo</a>
      <a href="#professor">Professor</a>
      <a href="#duvidas">Dúvidas</a>
      <a href="/">Pr. Rodrigo Mocellin</a>
      <a href="#inscrever" class="btn btn-accent bf-off">Quero me inscrever</a>
      <a href="#inscrever" class="btn btn-gold bf-only">Black Friday -{pct}%</a>
    </nav>
    <button class="menu-btn" id="menuBtn" aria-label="Abrir menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 8h16M4 16h16"/></svg></button>
  </div>
</header>

<main id="inicio">
<section class="lp-hero">
  <div class="lp-copy">
    <span class="label">{e(nome)} · Curso online</span>
    <h1>{e(d["sub"])}</h1>
    <p class="lead">{e(d["lead"])}</p>
    <div class="lp-price">
      <div class="bf-off"><b>R$ {oficial},00</b><span>{x_oficial}</span></div>
      <div class="bf-only bfp"><span class="tag">Black Friday -{pct}%</span><div><s>R$ {oficial},00</s><b>R$ {promo},00</b></div><span>ou em até 12x no cartão</span></div>
    </div>
    <div class="lp-actions">
      <a href="#inscrever" class="btn btn-accent bf-off">Quero me inscrever {SETA}</a>
      <a href="#inscrever" class="btn btn-gold bf-only">Garantir o desconto {SETA}</a>
      <a href="#conteudo" class="btn btn-ghost">Ver o conteúdo</a>
    </div>
    <div class="lp-feats">{feats}</div>
  </div>
  <div class="lp-photo"><img src="/assets/img/{foto}.jpg" width="1000" height="753" alt="" fetchpriority="high">{quote}</div>
</section>

<section class="bfs bf-only" aria-label="Black Friday">
  <div class="wrap">
    <div class="bfs-t">Black<br>Friday</div>
    <div class="bfs-p">De <s>R$ {oficial},00</s> por<b>R$ {promo},00<em>-{pct}%</em></b>ou em até 12x no cartão</div>
    <div class="bfs-r">
      <div class="bfx-clock bf-timer"><div class="l">A oferta termina em</div>{cd()}</div>
      {comprar("Garantir com desconto", "btn btn-gold")}
    </div>
  </div>
</section>

<section class="sec" id="curso">
  <div class="wrap about-c">
    <div class="fade">
      <span class="label">Sobre o curso · {e(publico)}</span>
      <h2>{e(d["about_h2"])}</h2>
      <p>{e(d["about_p"])}</p>
    </div>
    <div class="points fade">{pontos}</div>
  </div>
</section>

<section class="sec dark" id="conteudo">
  <div class="wrap">
    <div class="sec-head fade"><div><span class="label">Conteúdo do curso</span><h2>{e(d["mods_h2"])}</h2></div><p>Assista no seu ritmo, pelo celular, tablet ou computador.</p></div>
    <div class="mods">{mods}</div>
    <div class="center-cta"><a href="#inscrever" class="btn btn-accent">Quero acessar todos os módulos {SETA}</a></div>
  </div>
</section>

<section class="sec" id="professor">
  <div class="wrap prof">
    <img class="fade" src="/assets/img/professor.jpg" width="1000" height="563" loading="lazy" alt="Pr. Rodrigo Mocellin">
    <div class="fade">
      <span class="label">Quem ensina</span>
      <h2>Pr. Rodrigo Mocellin</h2>
      {profp}
      <div class="prof-facts">{facts}</div>
      <a href="/" class="arrow-link">Conheça o ministério {SETA}</a>
    </div>
  </div>
</section>

<section class="sec" id="depoimentos" style="background:var(--paper-2)">
  <div class="wrap">
    <div class="sec-head fade"><div><span class="label">Depoimentos</span><h2>{e(d["depos_h2"])}</h2></div></div>
    <div class="depos">{depos}</div>
  </div>
</section>

<section class="sec dark" id="inscrever">
  <div class="wrap invest">
    <div class="fade">
      <span class="label">Investimento</span>
      <h2>{e(d["invest_h2"])}</h2>
      <div class="incl">{incl}</div>
    </div>
    <div class="pcard fade">
      <div class="lbl">{e(nome)}</div>
      <h3>Curso completo</h3>
      <div class="acc">Acesso por 12 meses</div>
      <div class="bf-only"><span class="tag">Black Friday · {pct}% OFF</span><div class="de">De <s>R$ {oficial},00</s> por</div></div>
      <div class="now bf-off"><small>R$ </small>{oficial}<small>,00</small></div>
      <div class="x bf-off">{x_oficial}</div>
      <div class="now bf-only"><small>R$ </small>{promo}<small>,00</small></div>
      <div class="x bf-only">ou em até 12x no cartão</div>
      <div class="bfx-clock bf-timer bf-only"><div class="l">Oferta termina em</div>{cd()}</div>
      {comprar("Quero me inscrever")}
      <div class="sec-note">{CADEADO} Pagamento 100% seguro</div>
    </div>
  </div>
</section>

<section class="sec" id="duvidas">
  <div class="wrap">
    <div class="sec-head fade"><div><span class="label">Perguntas frequentes</span><h2>Dúvidas mais comuns</h2></div><p>Outra dúvida? Escreva para <a href="mailto:{e(d["email"])}" style="border-bottom:1.5px solid currentColor">{e(d["email"])}</a></p></div>
    <div class="faq fade">{faq}</div>
  </div>
</section>

<section class="dark final">
  <div class="wrap fade">
    <h2>{e(d["cta_h"])}</h2>
    <p class="bf-off">{e(d["cta_p"])}</p>
    <p class="bf-only bf-timer">O preço de Black Friday acaba em {cd(True)}</p>
    {comprar("Quero iniciar meus estudos")}
    <div class="more"><span style="width:100%;font-size:.9rem;color:rgba(255,255,255,.55)">Conheça também</span>{outros}</div>
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="wrap foot">
    <span>© 2026 {e(nome)} · Pr. Rodrigo Mocellin</span>
    <nav><a href="/">Início</a><a href="/#cursos">Todos os cursos</a><a href="mailto:{e(d["email"])}">{e(d["email"])}</a></nav>
  </div>
</footer>
<script src="/assets/site.js"></script>
</body>
</html>
'''


if __name__ == "__main__":
    dados = json.load(open(os.path.join(RAIZ, "ferramentas", "cursos.json"), encoding="utf-8"))
    for slug in CONFIG:
        html = pagina(slug, dados[slug])
        with open(os.path.join(RAIZ, slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("ok", slug, len(html) // 1024, "KB")
