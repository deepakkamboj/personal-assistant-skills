// Generates website/data/catalog.json from the real SKILL.md frontmatter under ../.agents/skills so
// the docs never drift from the library. Runs automatically before `dev` and `build`.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.join(__dirname, "..", "..");
const SKILLS_DIR = path.join(REPO_ROOT, ".agents", "skills");
const OUT = path.join(__dirname, "..", "data", "catalog.json");

const GROUP_LABELS = {
  core: "Core skills",
  email: "Email",
  writing: "Writing",
  linkedin: "LinkedIn",
};

function walk(dir, match) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(p, match));
    else if (match(e.name)) out.push(p);
  }
  return out;
}

function frontmatter(text) {
  const m = text.replace(/\r\n/g, "\n").match(/^---\n([\s\S]*?)\n---/);
  const o = {};
  if (m) {
    for (const line of m[1].split("\n")) {
      const kv = line.match(/^([A-Za-z_-]+):\s*(.*)$/);
      if (kv) o[kv[1]] = kv[2].trim().replace(/^["']|["']$/g, "");
    }
  }
  return o;
}

const skills = walk(SKILLS_DIR, (n) => n === "SKILL.md")
  .map((f) => {
    const meta = frontmatter(fs.readFileSync(f, "utf8"));
    const rel = path.relative(SKILLS_DIR, path.dirname(f)).split(path.sep);
    const group = rel.length === 1 ? "core" : rel[0];
    return {
      group,
      groupLabel: GROUP_LABELS[group] || group,
      name: meta.name || rel[rel.length - 1],
      description: meta.description || "",
    };
  })
  .sort((a, b) => a.group.localeCompare(b.group) || a.name.localeCompare(b.name));

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify({ skills }, null, 2) + "\n");
console.log(`Wrote ${path.relative(REPO_ROOT, OUT)} — ${skills.length} skills.`);
