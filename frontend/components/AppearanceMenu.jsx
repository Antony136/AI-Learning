import { useEffect, useRef, useState } from "react";

function AppearanceMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const [theme, setTheme] = useState(() => localStorage.getItem("rag_app_theme") || "dark");
  const [textSize, setTextSize] = useState(() => localStorage.getItem("rag_app_text_size") || "medium");
  const [fontFamily, setFontFamily] = useState(() => localStorage.getItem("rag_app_font_family") || "sans");

  const menuRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("rag_app_theme", theme);
  }, [theme]);

  useEffect(() => {
    document.documentElement.setAttribute("data-text-size", textSize);
    localStorage.setItem("rag_app_text_size", textSize);
  }, [textSize]);

  useEffect(() => {
    document.documentElement.setAttribute("data-font-family", fontFamily);
    localStorage.setItem("rag_app_font_family", fontFamily);
  }, [fontFamily]);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="appearance-menu-container" ref={menuRef}>
      <button
        type="button"
        className="appearance-toggle-button"
        aria-label="Appearance & Display Settings"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((prev) => !prev)}
        title="Customize Appearance"
      >
        <span className="appearance-icon">⚙️</span>
        <span className="appearance-button-text">Appearance</span>
        <span className="appearance-chevron">{isOpen ? "▲" : "▼"}</span>
      </button>

      {isOpen && (
        <div className="appearance-dropdown-menu" role="menu">
          <div className="appearance-menu-header">
            <h3>Display Settings</h3>
            <p>Customize view & text styles</p>
          </div>

          <div className="appearance-section">
            <label className="appearance-label">Theme</label>
            <div className="appearance-button-group">
              <button
                type="button"
                className={`appearance-option-btn ${theme === "dark" ? "active" : ""}`}
                onClick={() => setTheme("dark")}
              >
                🌙 Dark
              </button>
              <button
                type="button"
                className={`appearance-option-btn ${theme === "light" ? "active" : ""}`}
                onClick={() => setTheme("light")}
              >
                ☀️ Light
              </button>
              <button
                type="button"
                className={`appearance-option-btn ${theme === "midnight" ? "active" : ""}`}
                onClick={() => setTheme("midnight")}
              >
                🌌 Midnight
              </button>
            </div>
          </div>

          <div className="appearance-section">
            <label className="appearance-label">Text Size</label>
            <div className="appearance-button-group">
              <button
                type="button"
                className={`appearance-option-btn ${textSize === "small" ? "active" : ""}`}
                onClick={() => setTextSize("small")}
              >
                Small
              </button>
              <button
                type="button"
                className={`appearance-option-btn ${textSize === "medium" ? "active" : ""}`}
                onClick={() => setTextSize("medium")}
              >
                Medium
              </button>
              <button
                type="button"
                className={`appearance-option-btn ${textSize === "large" ? "active" : ""}`}
                onClick={() => setTextSize("large")}
              >
                Large
              </button>
            </div>
          </div>

          <div className="appearance-section">
            <label className="appearance-label">Font Style</label>
            <div className="appearance-button-group">
              <button
                type="button"
                className={`appearance-option-btn ${fontFamily === "sans" ? "active" : ""}`}
                onClick={() => setFontFamily("sans")}
                style={{ fontFamily: "sans-serif" }}
              >
                Sans-Serif
              </button>
              <button
                type="button"
                className={`appearance-option-btn ${fontFamily === "serif" ? "active" : ""}`}
                onClick={() => setFontFamily("serif")}
                style={{ fontFamily: "serif" }}
              >
                Serif
              </button>
              <button
                type="button"
                className={`appearance-option-btn ${fontFamily === "mono" ? "active" : ""}`}
                onClick={() => setFontFamily("mono")}
                style={{ fontFamily: "monospace" }}
              >
                Monospace
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AppearanceMenu;
