import React, { useState } from "react";
import LanguageToggle from "./LanguageToggle";

const Header: React.FC = () => {
  const [language, setLanguage] = useState("mf");

  return (
    <div
      style={{
        width: "800px",
        height: "60px",
        backgroundColor: "#0078d4",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 20px",
        borderRadius: "10px 10px 0 0",
        color: "white",
        fontSize: "1.5rem",
        fontWeight: "bold",
      }}
    >
      SICT Local ChatBot
      <LanguageToggle language={language} setLanguage={setLanguage} />
    </div>
  );
};

export default Header;
