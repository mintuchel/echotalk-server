import React from "react";
import ChatbotUI from "./components/ChatbotUI";
import Header from "./components/Header";
import DateLabels from "./components/DateLabels";

const App: React.FC = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        position: "relative",
      }}
    >
      <DateLabels />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          height: "100%",
          position: "relative",
        }}
      >
        <Header />
        <ChatbotUI />
      </div>
    </div>
  );
};

export default App;
