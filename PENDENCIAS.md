# Pendências antes de divulgar o site

Site publicado a partir dos HTMLs prontos, um por curso, com URLs limpas:

- `/` — site institucional (cd187510-Site_Rodrigo_Mocellin.html)
- `/sexualidadecrista/`
- `/homeschooling/`
- `/criacaodefilhos/`
- `/culpadomeucorpo/`
- `/mentecrista/`

## 1. Links de pagamento (botões "Quero me inscrever" / "Quero iniciar meus estudos")

Todos apontam para `href="#"` por enquanto. Localizar com:

```
grep -n 'href="#" class="btn btn-gold"' */index.html
```

- `sexualidadecrista/index.html` — **2 botões** (um na seção de preço, outro no banner final "Comece agora sua jornada")
- `homeschooling/index.html` — 1 botão
- `criacaodefilhos/index.html` — 1 botão
- `culpadomeucorpo/index.html` — 1 botão
- `mentecrista/index.html` — 1 botão

## 2. WhatsApp

Não há nenhum botão/link de WhatsApp nos HTMLs enviados (nem flutuante, nem no rodapé). Precisamos do número para adicionar.

## 3. Página `/livraria/`

O menu do site institucional (`index.html`) e das landing pages linka para `/livraria/`, mas esse HTML não foi enviado. Enquanto não existir, o link dá 404.

## 4. Links "Ler mais →" dos artigos

Nas seções de artigos de cada landing page, os links "Ler mais →" também são `href="#"` (não é link de pagamento, mas fica registrado).

## 5. Contato

E-mail já presente no site institucional: `contato@rodrigomocellin.com.br`.
