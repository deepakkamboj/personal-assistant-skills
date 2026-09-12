import React from "react";
import catalog from "../data/catalog.json";

type Skill = { group: string; groupLabel: string; name: string; description: string };

export default function SkillsTable() {
  const skills = (catalog.skills as Skill[]) || [];
  const order = ["core", "email", "writing", "linkedin"];
  const groups: Record<string, Skill[]> = {};
  for (const s of skills) (groups[s.group] ||= []).push(s);
  const names = Object.keys(groups).sort(
    (a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99) || a.localeCompare(b)
  );

  return (
    <div className="das-catalog">
      {names.map((g) => (
        <section key={g}>
          <h2>
            {groups[g][0]?.groupLabel || g}{" "}
            <span style={{ color: "#9ca3af", fontWeight: 400, fontSize: "0.9rem" }}>
              ({groups[g].length})
            </span>
          </h2>
          <table>
            <thead>
              <tr>
                <th style={{ width: 190 }}>Skill</th>
                <th>What it does</th>
              </tr>
            </thead>
            <tbody>
              {groups[g].map((s) => (
                <tr key={s.name}>
                  <td>
                    <code>{s.name}</code>
                  </td>
                  <td>{s.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ))}
    </div>
  );
}
