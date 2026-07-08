---
description: Generate a professional README.md and MIT LICENSE for this project. Auto-detects the tech stack (Python/C/C++/Java/C#/HTML/Node/LaTeX...), writes GitHub-ready docs with Damian Dominiak branding. Use when the repo needs an attractive README for people browsing GitHub / GitHub Pages.
---

# Workflow: generate README.md + LICENSE

You are a senior engineer writing documentation for a **public GitHub repository** that people will browse (and possibly see on GitHub Pages). Produce a README that is honest, technical, well-structured and visually attractive with shields.io badges. Work only from real project data — never invent features, benchmarks or results.

## Step 0 — Scope (do this first, strictly)

- The target project is **the currently open workspace / project root** — the folder you were invoked in.
- **Write `README.md` and `LICENSE` ONLY in that root.** Never write into a parent, sibling, or any other project directory.
- **Read only files inside this project root.** Do NOT scan or edit unrelated folders next to it, even if they look like similar projects.
- If the root is ambiguous (e.g. multiple projects are open), ask the user which folder is the target before writing anything.

## Step 1 — Detect the project

Read what actually exists in the repo and infer the stack. Do NOT assume it is a web/React project.

- **Language / build files:** `package.json` (Node/JS/TS), `requirements.txt` / `pyproject.toml` / `setup.py` (Python), `pom.xml` / `build.gradle` (Java), `*.csproj` / `*.sln` (C#/.NET), `Makefile` / `CMakeLists.txt` (C/C++), `Cargo.toml` (Rust), `go.mod` (Go), `index.html` (static site), `*.tex` (LaTeX), `Dockerfile`, `docker-compose.yml`.
- **Extract:** project name (from the repo/folder name or manifest), short description, entry point(s), how to install/build/run, main dependencies, and whether it deploys to **GitHub Pages** (an `index.html`, a `docs/` folder, or a `gh-pages` setup).
- **Scan the source** briefly to describe what the project actually does and its key features.
- If something essential is missing (e.g. no description anywhere), ask the user ONE short question rather than guessing.

### Then gather what the files CANNOT tell you (ask the user briefly, before writing)

Two high-impact details rarely live in the code — you must ask, not assume. Ask the user **in Polish**, in one short message:

- **Live / demo URL?** If a git remote points to `github.com/<user>/<repo>`, the project may be on **GitHub Pages** at
  `https://<user>.github.io/<repo>/` — propose that exact URL and ask them to confirm (never assume it's live).
  Example (PL): *„Czy projekt jest gdzieś opublikowany (GitHub Pages / live URL)? Zgaduję, że to `https://<user>.github.io/<repo>/` — potwierdź, popraw albo powiedz, że nie ma."*
- **Screenshot or GIF?** Example (PL): *„Masz screenshot lub krótki GIF aplikacji? Podaj ścieżkę / wrzuć plik do repo, albo powiedz, że pomijamy."*

Use whatever they give you; skip cleanly what they don't. A **confirmed live URL becomes a prominent CTA** in the
hero and the first step in Getting Started. If the user doesn't reply or has neither, proceed without them (no placeholders).

## Step 2 — Back up any existing README

If `README.md` exists, copy it to `README.backup.md` first. Never destroy the user's work silently.

## Step 3 — Write README.md (this is the project's shop-front — make it WOW)

This README is the first thing people see on the repo / GitHub Pages. Within ~3 seconds a visitor should think
**"this looks professional, and this project is for me"** — while everything stays 100% honest. Lead with
**benefits and real numbers**, make it **visually striking**, and put a clear **call to action** near the top.

Structure (adapt to the project; drop what doesn't apply):

1. **Centered hero** — wrap in `<div align="center"> … </div>`:
   - **Inside the centered div use raw HTML** (`<h1>`, `<h3>`/`<p>`, `<a>`) for the title, tagline and demo link —
     NOT markdown `#` / `### ` / `[text](url)` — otherwise many renderers show them as literal text. Badges stay as `<img>`/`<a>`.
   - Project title (optionally one leading emoji).
   - A **benefit-led one-liner** that sells the value, not the mechanics, using **real numbers pulled from the
     project** (e.g. "158 practice questions") — never invented. Keep it **positive and neutral**: do NOT lead with
     legally-sensitive framing (e.g. "extracted from exam dumps") — any such caveat belongs only in the Disclaimer.
   - **Add a stat badge for EACH meaningful headline number** you can find (question/item/record count, exhibits,
     components, endpoints, coverage, supported formats…) — aim for **2-4 stat badges** (e.g. `Questions-158`,
     `Exhibits-17`), not just one — alongside the tech badges and a `License MIT` badge (`?style=for-the-badge`, accent `1e90b8`).
   - If a **live / demo URL** is known or confirmed (from the user, or a GitHub Pages URL they confirmed): a prominent
     **▶ Live demo** button right here, and make "use the live demo" the **first option** in Getting Started.
2. **Screenshot or GIF** — near the very top; the single biggest "wow" element (only if a real image is available):
   - If the repo already contains a screenshot/GIF (`docs/`, `screenshots/`, `assets/`, `.github/`), embed it centered (`width` ≈ 800).
   - If none exists (and you didn't already get an answer in the Step-1 questions), **ask the user once, in Polish**: *„Masz screenshot lub krótki GIF aplikacji? Podaj ścieżkę / wrzuć plik do repo — albo powiedz, że pomijamy."*
     - If they provide a real file → embed it centered.
     - If they decline, don't answer, or have none → **omit the screenshot section entirely.**
   - **Never** insert a placeholder image, an invented path, or a link to a file that doesn't exist — it would show as a broken image on GitHub. No screenshot is better than a broken one.
3. **Why / value** — 2–3 sentences: the problem it solves and why someone should care (benefit-first, honest).
4. **Features** — a **table or grid with emojis**, each item phrased as a **benefit** ("💾 Progress that sticks — saved
   between sessions"), not a flat dry list. **Aim for 6-10 real features** — dig through the code to surface the
   non-obvious ones (local persistence / `localStorage`, search & filter, randomisation, offline / zero-dependencies,
   responsive & mobile, keyboard or accessibility niceties, an API / CLI, automated tooling / scripts…), not just the
   obvious three. **Real features only** — never pad the list with invented ones.
5. **Getting started** — prerequisites + exact install/build/run commands for the DETECTED stack. Examples:
   - Python: `python -m venv .venv` → `pip install -r requirements.txt` → `python main.py`
   - C/C++: `cmake -B build && cmake --build build` or `make` → run the binary
   - Java: `mvn package` / `./gradlew build` → `java -jar ...`
   - Node: `npm install` → `npm run dev` / `npm start`
   - Static site: open `index.html` or the GitHub Pages URL
6. **Usage / examples** — short code block or screenshot placeholder if useful.
7. **Live demo** — only if GitHub Pages / a homepage exists: link it.
8. **Project structure** — a short tree of the important folders/files.
9. **Roadmap / TODO** — only if there are clear next steps.
10. **License** — one line pointing to the MIT LICENSE.
11. **Author** — the block below.

### Author block (use verbatim, adjust only if the user provides new data)

```markdown
## 👤 Author

**Damian Dominiak** — Technical Computer Science student @ Wrocław University of Science and Technology.
Linux · Infrastructure · Embedded · Networking.

[![GitHub](https://img.shields.io/badge/GitHub-domino0472-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/domino0472)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Damian_Dominiak-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/damian-dominiak/)
[![Email](https://img.shields.io/badge/Email-damian.dominiak.2006@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:damian.dominiak.2006@gmail.com)

<sub>Built with Linux, C and coffee ☕</sub>
```

## Step 4 — Write LICENSE (MIT)

Create a `LICENSE` file with the standard MIT text:

```
MIT License

Copyright (c) 2026 Damian Dominiak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Rules

- **Real data only.** Never invent metrics, features or results. Being **confident and benefit-led** is encouraged (this is a shop-front) — but every single claim must be true.
- **Visual "wow" where possible:** centered hero, real-number stat badges, and a prominent live-demo CTA if it deploys. A **screenshot/GIF near the top** is the highest-impact element — embed an existing one, or ask the user for one; if none is available, skip that section cleanly. **Never leave a broken image, placeholder, or dead path in the repo** — no screenshot beats a broken one.
- **Language:** **Talk to the user in Polish** — every question, confirmation and summary you show them is written in Polish. But **write the README and LICENSE content in English** by default (international GitHub audience). Only switch the document to Polish if the user explicitly asks for a Polish README.
- **Accent color** `1e90b8`, badge style `for-the-badge`, consistent with Damian's GitHub profile.
- **License:** MIT only (single, permissive) — appropriate for open personal/academic projects.
- **Year:** 2026.
- **Stay in scope (Step 0):** `README.md` and `LICENSE` are written only in the current project root; never touch neighbouring folders.
- **Disclaimer when needed:** if the project builds on third-party or trademarked material (e.g. exam questions/dumps, a dataset, a vendor's product), add a short **Disclaimer** section — state it is unofficial, name the trademark owner, and add "not affiliated with or endorsed by <owner>".
- **Don't duplicate badges:** the hero already shows badges; in the Tech stack section give a short labelled list (Frontend / Tooling), not a second identical badge row.
- After writing, show the user a one-line summary of what was detected and generated, and remind them to review before pushing.
