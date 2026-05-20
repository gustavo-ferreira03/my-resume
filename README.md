# Resume Manager

Pipeline simples para manter dados de curriculo em YAML e gerar um curriculo em LaTeX/PDF.

O projeto evita edicao manual de `.tex`: voce edita `data/output/latex/resume-data.yml`, roda um comando, e o template gera o `.tex` e o `.pdf` finais.

## Como Funciona

```txt
data/output/latex/resume-data.yml
  + templates/output/latex/curriculo_template.tex
  -> pnpm run build-resume
  -> data/output/latex/[output_filename].tex
  -> data/output/latex/[output_filename].pdf
```

## Comeco Rapido

```bash
pnpm install
pnpm run build-resume
```

O PDF sera gerado em `data/output/latex/`, usando o valor de `output_filename` definido no YAML.

## Estrutura

```txt
data/output/latex/
  resume-data.yml          Dados do curriculo. Edite este arquivo.
  [nome].tex               Gerado automaticamente. Nao edite.
  [nome].pdf               PDF final.

templates/output/latex/
  curriculo_template.tex   Template LaTeX com placeholders.

scripts/
  build-resume.ts          Valida YAML, renderiza LaTeX e compila PDF.
```

## Dados Do Curriculo

O arquivo principal e `data/output/latex/resume-data.yml`.

Campos principais:

```yaml
personal:
  name: Seu Nome
  title: Seu Cargo
  email: seu@email.com
  linkedin_url: https://linkedin.com/in/seu-usuario
  github_url: https://github.com/seu-usuario

experience:
  - company: Empresa
    period:
      from: Jan 2023
      to: Atual
    role: Cargo
    url: https://empresa.com
    bullets:
      - Desenvolvi uma funcionalidade com **destaque em negrito**.

projects: []

skills:
  - label: Backend
    items: TypeScript, Node.js, PostgreSQL

education:
  - institution: Universidade
    period:
      from: Jun 2021
      to: Dez 2026
    degree: Bacharelado em Ciencia da Computacao
    location: Niteroi, RJ

output_filename: curriculo_nome
```

## Formatacao De Bullets

Use marcadores simples no YAML:

| YAML | LaTeX gerado |
|---|---|
| `**texto**` | `\textbf{texto}` |
| `_texto_` | `\textit{texto}` |

Nao escreva LaTeX bruto dentro do YAML.

## Scripts

```bash
pnpm run build-resume
```

Esse comando:

1. Compila o TypeScript.
2. Valida `resume-data.yml` com Zod.
3. Renderiza o template LaTeX.
4. Compila o PDF com `pdflatex`.
5. Remove arquivos auxiliares do LaTeX.

## Privacidade

`data/` fica fora do Git por padrao, porque contem informacoes pessoais e arquivos gerados.

## Licenca

MIT - Gustavo Cosme
