#!/usr/bin/env node
"use strict";

/**
 * personal-assistant-skills CLI.
 *
 * Commands:
 *   init [--dir <path>] [--force]   Create config.json/content.md/memory.md/notes.md from templates
 *   path                            Print the installed .agents directory
 *   list                            List available skills
 *   install <targetDir> [--force]   Copy the .agents tree into <targetDir> (embed in a repo)
 *   help                            Show usage
 */

const fs = require("fs");
const os = require("os");
const path = require("path");

const PKG_ROOT = path.join(__dirname, "..");
const AGENTS_DIR = path.join(PKG_ROOT, ".agents");
const CONFIG_DIR = path.join(AGENTS_DIR, "config");

const TEMPLATES = [
  ["config.example.json", "config.json"],
  ["content.example.md", "content.md"],
  ["memory.example.md", "memory.md"],
  ["notes.example.md", "notes.md"],
];

function parseFlags(args) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    } else {
      positional.push(args[i]);
    }
  }
  return { flags, positional };
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function init(flags) {
  const dir = flags.dir
    ? path.resolve(flags.dir)
    : path.join(os.homedir(), ".assistant");
  fs.mkdirSync(dir, { recursive: true });

  let created = 0;
  let skipped = 0;
  for (const [tpl, out] of TEMPLATES) {
    const target = path.join(dir, out);
    if (fs.existsSync(target) && !flags.force) {
      console.log(`  skip  ${out} (exists; use --force to overwrite)`);
      skipped++;
      continue;
    }
    fs.copyFileSync(path.join(CONFIG_DIR, tpl), target);
    console.log(`  create ${out}`);
    created++;
  }

  const configPath = path.join(dir, "config.json");
  console.log(`\n  Config location: ${dir}`);
  console.log(`  Created ${created}, skipped ${skipped}.`);
  console.log("\n  Next: point ASSISTANT_CONFIG at your config, e.g.");
  if (process.platform === "win32") {
    console.log(`    setx ASSISTANT_CONFIG "${configPath}"`);
  } else {
    console.log(`    export ASSISTANT_CONFIG="${configPath}"`);
  }
  console.log("\n  Then edit config.json (profile, brand, sources) and content.md (voice, prompts).");
  console.log("  See CONFIGURATION.md for the full schema.\n");
}

function listSkills() {
  const skillsRoot = path.join(AGENTS_DIR, "skills");
  const found = [];
  const walk = (dir, prefix) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const full = path.join(dir, entry.name);
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (fs.existsSync(path.join(full, "SKILL.md"))) found.push(rel);
      walk(full, rel);
    }
  };
  walk(skillsRoot, "");
  found.sort();
  console.log(`\n  ${found.length} skills:\n`);
  for (const s of found) console.log(`   - ${s}`);
  console.log("");
}

function install(positional, flags) {
  const target = positional[0];
  if (!target) {
    console.error("  Usage: assistant-skills install <targetDir>");
    process.exit(1);
  }
  const base = path.resolve(target);
  const jobs = [
    [AGENTS_DIR, path.join(base, ".agents")],
    [path.join(PKG_ROOT, ".claude", "commands"), path.join(base, ".claude", "commands")],
    [path.join(PKG_ROOT, ".github", "prompts"), path.join(base, ".github", "prompts")],
  ];
  for (const [src, dest] of jobs) {
    if (!fs.existsSync(src)) continue;
    if (fs.existsSync(dest) && !flags.force) {
      console.error(`  ${dest} already exists. Use --force to overwrite.`);
      process.exit(1);
    }
    copyDir(src, dest);
    console.log(`  Copied ${path.relative(PKG_ROOT, src)} -> ${dest}`);
  }
  console.log("\n  Slash commands installed: /assistant:me, /assistant:linkedin, /assistant:post, ... in Claude Code");
  console.log("  (GitHub Copilot uses /assistant-me, /assistant-linkedin, ... since it has no ':' namespace).");
}

function help() {
  console.log(`
  personal-assistant-skills

  Usage:
    assistant-skills init [--dir <path>] [--force]   Create config from templates (default ~/.assistant)
    assistant-skills path                            Print the installed .agents directory
    assistant-skills list                            List available skills
    assistant-skills install <dir> [--force]         Copy the .agents tree into a project
    assistant-skills help                            Show this help
`);
}

function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const { flags, positional } = parseFlags(rest);
  switch (cmd) {
    case "init":
      return init(flags);
    case "path":
      return console.log(AGENTS_DIR);
    case "list":
      return listSkills();
    case "install":
      return install(positional, flags);
    case "help":
    case undefined:
      return help();
    default:
      console.error(`  Unknown command: ${cmd}`);
      help();
      process.exit(1);
  }
}

main();
