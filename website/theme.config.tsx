import React from "react";
import type { DocsThemeConfig } from "nextra-theme-docs";

const config: DocsThemeConfig = {
  logo: (
    <span style={{ fontWeight: 700 }}>
      personal-<span style={{ color: "#6366f1" }}>assistant</span>-skills
    </span>
  ),
  project: {
    link: "https://github.com/deepakkamboj/personal-assistant-skills",
  },
  docsRepositoryBase:
    "https://github.com/deepakkamboj/personal-assistant-skills/tree/main/website",
  footer: {
    content: (
      <span>
        Open-source · MIT ·{" "}
        <a href="https://github.com/deepakkamboj/personal-assistant-skills">
          github.com/deepakkamboj/personal-assistant-skills
        </a>
      </span>
    ),
  },
  head: (
    <>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta
        name="description"
        content="Vendor-neutral personal-assistant plugin for Claude Code, GitHub Copilot, and Codex — AI digest, daily briefing, personal branding, LinkedIn toolkit, newsletters, writing quality, and visual artifacts."
      />
    </>
  ),
  color: { hue: 245, saturation: 75 },
  darkMode: true,
};

export default config;
