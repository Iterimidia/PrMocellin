# PrMocellin

Site estático do Pr. Rodrigo Mocellin, publicado no Netlify a partir da raiz do repositório.

- `/` — home (`index.html`)
- `/sexualidadecrista/`, `/homeschooling/`, `/criacaodefilhos/`, `/culpadomeucorpo/`, `/mentecrista/` — páginas de curso

## Onde mexer

- **Black Friday (datas e links promocionais):** `black-friday.js`. Fora do período, o site mostra sozinho os preços e links oficiais. Prévia: `?bf=1` (desliga com `?bf=0`).
- **Estilo compartilhado:** `assets/site.css` (todas as páginas) e `assets/curso.css` (páginas de curso).
- **Imagens:** `assets/img/`.
- **Páginas de curso:** são geradas. Edite os textos em `ferramentas/cursos.json` e os preços/cores em `ferramentas/gerar_cursos.py`, depois rode:

  ```
  python3 ferramentas/gerar_cursos.py
  ```
