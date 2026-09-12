# Website — Nextra documentation site

**Nextra 3** (`nextra-theme-docs`) documentation site for **personal-assistant-skills**,
static-exported and deployed to GitHub Pages.

**Live site:** https://deepakkamboj.github.io/personal-assistant-skills/

## Develop

```bash
cd website
npm install
npm run dev            # http://localhost:3000
```

## Build (static export)

```bash
# basePath is required for a GitHub project Pages site
NEXT_PUBLIC_BASE_PATH=/personal-assistant-skills npm run build
# static site is emitted to website/out/
```

## How the catalog stays accurate

`npm run prebuild` (auto-run before `dev`/`build`) executes `scripts/gen-catalog.mjs`, which reads the
real `SKILL.md` frontmatter from `../.agents/skills/` and writes `data/catalog.json`. The
`SkillsTable` component renders from that JSON, so the site never drifts.

## Structure

- `pages/*.mdx` — MDX content (index, getting-started, skills, capabilities) with `_meta.js`
- `components/` — `Home`, `Diagram`, `Features`, `Cards`, `PackageInstall`, `EnvTable`,
  `FileStructure`, `SkillsTable`, `icons`
- `public/*.svg` — hand-authored diagrams (architecture, skill-map, publish-flow)
- `theme.config.tsx` — Nextra docs theme configuration
- `styles/custom.css` — landing-page + catalog styling layered on the theme

## Deploy

`.github/workflows/pages.yml` builds this app with `NEXT_PUBLIC_BASE_PATH` set and publishes
`website/out` via `actions/deploy-pages`. Enable **Settings → Pages → Source: GitHub Actions** once.
