import React from "react";
import ChatbotUI from "./components/ChatbotUI";

const App: React.FC = () => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <ChatbotUI />
    </div>
  );
};

export default App;
