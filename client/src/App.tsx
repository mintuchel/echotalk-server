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
        <h2>Local ChatBot</h2>
      </div>
      <ChatbotUI />
    </div>
  );
};

export default App;
