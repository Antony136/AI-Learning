import { useState } from "react";


function CopyButton({
  text,
  getText,
  className = ""
}) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      const value = getText
        ? getText()
        : text;

      await navigator.clipboard.writeText(value);

      setCopied(true);

      window.setTimeout(() => {
        setCopied(false);
      }, 1600);

    } catch (error) {
      console.error(
        "Could not copy text.",
        error
      );
    }
  }

  return (
    <button
      type="button"
      className={`copy-button ${className}`}
      onClick={handleCopy}
      aria-label={
        copied
          ? "Copied"
          : "Copy"
      }
    >
      {copied
        ? "Copied"
        : "Copy"}
    </button>
  );
}


export default CopyButton;