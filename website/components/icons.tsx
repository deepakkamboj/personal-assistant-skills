import React from "react";

const base = {
  width: "100%",
  height: "100%",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export const SparkleIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" />
    <path d="M18 15l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z" />
  </svg>
);

export const SunIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
  </svg>
);

export const UserIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <circle cx="12" cy="8" r="4" />
    <path d="M4 21c0-4 3.6-7 8-7s8 3 8 7" />
  </svg>
);

export const LinkedInIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <rect x="3" y="3" width="18" height="18" rx="2" />
    <path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 0 1 4 0v4M11 17v-7" />
  </svg>
);

export const MailIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <rect x="3" y="5" width="18" height="14" rx="2" />
    <path d="M3 7l9 6 9-6" />
  </svg>
);

export const PenIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <path d="M16 3l5 5L8 21H3v-5z" />
    <path d="M14 5l5 5" />
  </svg>
);

export const ImageIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <rect x="3" y="4" width="18" height="16" rx="2" />
    <circle cx="9" cy="10" r="2" />
    <path d="M21 17l-5-5-6 6" />
  </svg>
);

export const RocketIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <path d="M5 15c-1 1-1.5 4-1.5 4s3-.5 4-1.5" />
    <path d="M9 15l-1-1c0-4 3-9 12-11-2 9-7 12-11 12l-1-1z" />
    <circle cx="14.5" cy="9.5" r="1.4" />
  </svg>
);

export const BookIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z" />
    <path d="M19 3v18" />
  </svg>
);

export const PlugIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <path d="M9 2v6M15 2v6" />
    <path d="M7 8h10v3a5 5 0 0 1-10 0z" />
    <path d="M12 16v6" />
  </svg>
);

export const CalendarIcon = () => (
  <svg viewBox="0 0 24 24" {...base}>
    <rect x="3" y="4" width="18" height="17" rx="2" />
    <path d="M3 9h18M8 2v4M16 2v4" />
  </svg>
);
