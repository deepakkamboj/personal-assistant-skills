import React from "react";
import { asset } from "./base";

export default function Diagram({
  src,
  alt,
  caption,
}: {
  src: string;
  alt: string;
  caption?: React.ReactNode;
}) {
  return (
    <figure className="das-figure">
      <img src={asset(src)} alt={alt} />
      {caption ? <figcaption>{caption}</figcaption> : null}
    </figure>
  );
}
