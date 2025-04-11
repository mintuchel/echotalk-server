import React, { useState } from "react";
import ChatbotUI from "./components/ChatbotUI";
import Header from "./components/Header";
import DateLabels from "./components/DateLabels";

const App: React.FC = () => {
  // ChatbotUI에 전달할 메시지들을 담는 상태변수
  // setMessages는 messages 상태를 업데이트하는 함수수
  const [messages, setMessages] = useState<any[]>([]);

  // DateLabels에서 클릭된 날짜들의 메시지들을 받아와 messages 상태를 업데이트하는 함수
  const handleDateSelect = (newMessages: any[]) => {
    setMessages(newMessages); // 선택된 날짜의 질문과 답변을 ChatbotUI에게 전달
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column", // ← 중요! 수평으로 배치
        height: "100vh",
        width: "100vw",
        position: "relative",
        border: "3px solid black"
      }}
    >
      {/* DateLabels 컴포넌트에게 handleDateSelect 함수를 Prop으로 전달*/}
      <DateLabels onDateSelect={handleDateSelect} />
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
        {/*ChatbotUI 컴포넌트에게 messages와 setMessages 두 개의 Prop을 전달*/}
        <ChatbotUI messages={messages} setMessages={setMessages} />
      </div>
    </div>
  );
};

export default App;
