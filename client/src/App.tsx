import React from "react";
import ChatbotUI from "./components/ChatbotUI";

const App: React.FC = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <div
        style={{
          padding: "0.5rem",
        }}
      >
        <div style={{ display: "flex" }}>
          <h2 style={{ color: "blue" }}>SICT</h2>
          <h2> Local ChatBot</h2>
        </div>
      </div>
      <ChatbotUI />
    </div>
  );
};

export default App;
