import React from "react";

interface LanguageToggleProps {
  language: string;
  setLanguage: (lang: string) => void;
}

const LanguageToggle: React.FC<LanguageToggleProps> = ({
  language,
  setLanguage,
}) => {
  return (
    <div
      style={{ marginRight: "1.5rem", display: "flex", alignItems: "center" }}
    >
      <label
        style={{
          marginRight: "0.5rem",
          fontSize: "1rem",
          fontWeight: "bold",
          border: "1px solid white",
          padding: "0.2rem 0.5rem",
          borderRadius: "5px",
        }}
      >
        LLM Model
      </label>
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        style={{
          padding: "0.5rem 1rem",
          fontSize: "1.2rem",
          borderRadius: "8px",
          border: "2px solid #007bff",
          backgroundColor: "#f8f9fa",
          cursor: "pointer",
          outline: "none",
          transition: "all 0.3s ease",
        }}
      >
        <option value="mf">Minfest</option>
        <option value="l3">llama3.3</option>
        <option value="g3">gemma3</option>
        <option value="ds">deepseek-r1</option>
      </select>
    </div>
  );
};

export default LanguageToggle;
