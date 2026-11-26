# AI Swiss Knife — Design & Curation Constitution (`v2.0.0-beta`)

This Field Book applies five proven information-design principles enforced automatically by `scripts/build.py lint`:

1. **Stone Librande (One-Page Design):** `README.md` serves as a single-screen Universal Compass connecting workload -> tier -> harness. Every chapter opens with a 1-glance Mermaid map highlighting relationships and physical bottlenecks.
2. **Edward Tufte (Small Multiples):** Every chapter uses the exact same **5-Beat Page Anatomy**:
   - Beat 1: Top/Bottom chapter breadcrumbs (`← Prev | 🏠 Cover | Next →`)
   - Beat 2: Inverted-pyramid `> [!IMPORTANT]` verdict + `Read this chapter if` trigger
   - Beat 3: Native GFM Mermaid relationship map
   - Beat 4: Strictly 4-column reference tables using `<br><sub>` typographic stacking and `<kbd>` badges
   - Beat 5: Collapsible `<details>` action drawers for copy-paste CLI recipes
3. **Katie Dill (Anti-Zombie Craft):** No neutral link dumps. Every entry requires benchmark/doc proof AND an explicit real-world catch (`⚠️ Gotcha`).
4. **Diátaxis Separation:** Reference facts live in tables; How-To recipes live in `<details>` drawers and `forage`; Explanations live in verdicts and `book/99-graveyard.md`.
5. **Dual Human + Agent Interface:** Humans read `README.md` + `book/*.md`; agents read `llms.txt` + `llms-full.txt`.
