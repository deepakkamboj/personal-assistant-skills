import React from "react";
import Link from "next/link";
import Diagram from "./Diagram";
import { Features, Feature } from "./Features";
import { Cards, Card } from "./Cards";
import { PackageInstall } from "./PackageInstall";
import {
  SparkleIcon,
  SunIcon,
  UserIcon,
  LinkedInIcon,
  MailIcon,
  PenIcon,
  ImageIcon,
  RocketIcon,
  BookIcon,
  PlugIcon,
} from "./icons";

const badges: [string, string, string][] = [
  ["npm version", "https://img.shields.io/npm/v/personal-assistant-skills?logo=npm&color=cb3837", "https://www.npmjs.com/package/personal-assistant-skills"],
  ["npm downloads", "https://img.shields.io/npm/dm/personal-assistant-skills?logo=npm", "https://www.npmjs.com/package/personal-assistant-skills"],
  ["CI", "https://github.com/deepakkamboj/personal-assistant-skills/actions/workflows/ci.yml/badge.svg", "https://github.com/deepakkamboj/personal-assistant-skills/actions/workflows/ci.yml"],
  ["License MIT", "https://img.shields.io/badge/License-MIT-green.svg", "https://github.com/deepakkamboj/personal-assistant-skills/blob/main/LICENSE"],
  ["Claude Code", "https://img.shields.io/badge/Claude_Code-ready-D97757?logo=anthropic&logoColor=white", "https://github.com/deepakkamboj/personal-assistant-skills"],
  ["GitHub Copilot", "https://img.shields.io/badge/GitHub_Copilot-ready-000000?logo=githubcopilot&logoColor=white", "https://github.com/deepakkamboj/personal-assistant-skills"],
  ["MCP", "https://img.shields.io/badge/MCP-connected--workspace-0A7EA4", "https://modelcontextprotocol.io"],
];

const stats: [string, string][] = [
  ["24", "Skills"],
  ["3", "Runtimes"],
  ["13", "LinkedIn tools"],
  ["1", "MCP server"],
];

export default function Home() {
  return (
    <div className="das-home">
      <section className="das-hero">
        <h1>Your personal brand &amp; productivity, on autopilot</h1>
        <p className="das-tagline">
          A vendor-neutral personal-assistant plugin for <strong>Claude Code</strong>,{" "}
          <strong>GitHub Copilot</strong>, and <strong>Codex</strong> — AI digests, daily briefings,
          personal branding, a full LinkedIn toolkit, newsletters, writing quality, and visual
          artifacts.
        </p>
        <div className="das-badges">
          {badges.map(([alt, src, href]) => (
            <a key={alt} href={href} target="_blank" rel="noreferrer">
              <img alt={alt} src={src} />
            </a>
          ))}
        </div>
        <div className="das-cta">
          <Link className="das-btn primary" href="/getting-started">
            Get started
          </Link>
          <Link className="das-btn ghost" href="/skills">
            Browse the skills
          </Link>
        </div>
      </section>

      <PackageInstall packages={["personal-assistant-skills"]} />

      <div className="das-stat-row">
        {stats.map(([n, l]) => (
          <div className="das-stat" key={l}>
            <div className="n">{n}</div>
            <div className="l">{l}</div>
          </div>
        ))}
      </div>

      <h2>What it does</h2>
      <Features>
        <Feature icon={<SparkleIcon />} title="Weekly AI digest">
          Researches the latest AI models, tools, papers, and products from your curated sources and
          produces a structured HTML digest with a personal editor&apos;s note.
        </Feature>
        <Feature icon={<SunIcon />} title="Daily briefing">
          Summarizes the day&apos;s email, chat, and calendar into one prioritized digest across
          Microsoft 365 and Google via the connected-workspace MCP.
        </Feature>
        <Feature icon={<UserIcon />} title="Personal branding">
          Generates bios, elevator pitches, headlines, and social posts in your authentic voice from
          your profile and writing samples.
        </Feature>
        <Feature icon={<LinkedInIcon />} title="LinkedIn toolkit">
          13 focused tools — posts, hooks, carousels, planning, reviews, repurposing, positioning,
          comments, connections, profile audits, and more.
        </Feature>
        <Feature icon={<MailIcon />} title="Email &amp; newsletters">
          Cold and follow-up emails with proven frameworks, plus a full newsletter system that sends
          via Gmail, deploys via FTP, and tracks engagement.
        </Feature>
        <Feature icon={<PenIcon />} title="Writing quality">
          Humanize stiff prose, and measure readability (Flesch-Kincaid, Gunning Fog, SMOG) and word
          stats with concrete recommendations.
        </Feature>
        <Feature icon={<ImageIcon />} title="Visual artifacts">
          The pixel skill creates diagrams, infographics, banners, slide decks, and charts as
          self-contained HTML or SVG using your brand tokens.
        </Feature>
      </Features>

      <h2>Explore</h2>
      <Cards cols={3}>
        <Card icon={<RocketIcon />} title="Getting started" href="/getting-started">
          Install, configure, and invoke skills from any runtime.
        </Card>
        <Card icon={<BookIcon />} title="Skills" href="/skills">
          All 24 skills, generated from the real frontmatter.
        </Card>
        <Card icon={<PlugIcon />} title="Capabilities" href="/capabilities">
          The connected-workspace MCP, templates, and runtimes.
        </Card>
      </Cards>

      <Diagram
        src="/architecture.svg"
        alt="Architecture: runtimes call thin adapters that resolve to the .agents canonical library, which reaches Gmail, Calendar, and LinkedIn through the connected-workspace MCP."
        caption="Runtimes → thin adapters → the .agents/ canonical library → connected-workspace MCP (Gmail · Calendar · LinkedIn) + FTP."
      />
    </div>
  );
}
