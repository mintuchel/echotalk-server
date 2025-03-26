import React, { useState, useRef } from "react";
import axios from "axios";
import styles from "./ChatbotUI.module.css";

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
}

/*
App.tsx에서 messages와 setMessages를 ChatbotUI에 전달합니다.

과거 채팅 내역을 DateLabels로부터 선택하여 messages 배열을 업데이트합니다.

이 배열은 ChatbotUI에서 props로 받아서 표시합니다.

ChatbotUI는 이제 messages를 props로 받지만, 사용자가 보낸 새로운 메시지는 setMessages를 통해 자신의 상태에 직접 추가합니다.

setMessages를 통해 새로운 메시지(사용자 메시지 및 봇의 응답)가 messages 배열에 추가됩니다.

**handleSendMessage**에서, 사용자가 메시지를 보내면 messages 배열에 직접 추가되고, 봇의 응답도 처리한 후 배열에 추가합니다.

useEffect 훅을 사용하여, messages가 업데이트될 때마다 스크롤을 자동으로 맨 아래로 이동시킵니다.
*/

// App.tsx에서 전달받은 Props
// 1. messages = App.tsx로부터 받은 메시지들
// 2. setMessages = messages 상태를 업데이트하는 함수
interface ChatbotUIProps {
  messages: Message[]; // App.tsx로부터 받은 messages
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>; // App.tsx에서 setMessages 전달
}

const ChatbotUI: React.FC<ChatbotUIProps> = ({ messages, setMessages }) => {
  const [inputMessage, setInputMessage] = useState("");
  const scrollViewRef = useRef<HTMLDivElement>(null);

  // 사용자 질문 처리
  const handleSendMessage = async () => {
    if (inputMessage.trim() === "") return;

    // 새 질문 생성하기기
    const userQuery: Message = {
      id: Date.now(),
      text: inputMessage.trim(),
      sender: "user",
    };

    // 사용자 메시지를 messages 배열에 추가
    setMessages((prevMessages) => [...prevMessages, userQuery]);

    setInputMessage("");

    // Chatbot 답변 기다리기
    await processUserQuery(inputMessage);

    if (scrollViewRef.current) {
      scrollViewRef.current.scrollTop = scrollViewRef.current.scrollHeight;
    }
  };

  // 사용자 질문에 대한 답변 처리
  async function processUserQuery(prompt: string) {
    try {
      const API_URL = "http://localhost:8000/ask";
      const response = await axios.post(API_URL, { prompt });
      const answerResponse = response.data;

      // Chatbot 응답을 message 배열에 추가
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: Date.now(), text: answerResponse.response, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  }

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messagesContainer} ref={scrollViewRef}>
        {messages.map((item) => (
          <div
            key={item.id}
            className={`${styles.message} ${styles[item.sender]}`}
          >
            {item.text}
          </div>
        ))}
      </div>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="메시지를 입력하세요"
          onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <button onClick={handleSendMessage}>전송</button>
      </div>
    </div>
  );
};

export default ChatbotUI;
