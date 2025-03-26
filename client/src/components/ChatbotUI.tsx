import React, { useState, useRef } from "react";
import axios from "axios";
import styles from "./ChatbotUI.module.css";

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
}

interface ChatbotUIProps {
  messages: Message[]; // App.tsx로부터 받은 messages
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>; // App.tsx에서 setMessages 전달
}

const ChatbotUI: React.FC<ChatbotUIProps> = ({ messages, setMessages }) => {
  const [inputMessage, setInputMessage] = useState("");
  const scrollViewRef = useRef<HTMLDivElement>(null);

  async function processUserQuery(prompt: string) {
    try {
      const API_URL = "http://localhost:8000/ask";
      const response = await axios.post(API_URL, { prompt });
      const answerResponse = response.data;

      // 사용자 메시지와 봇의 응답을 App.tsx로 전달
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: Date.now(), text: prompt, sender: "user" },
        { id: Date.now() + 1, text: answerResponse.response, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  }

  const handleSendMessage = async () => {
    if (inputMessage.trim() === "") return;

    // 사용자 메시지를 App.tsx로 전달하여 상태를 업데이트
    await processUserQuery(inputMessage);
    setInputMessage("");

    if (scrollViewRef.current) {
      scrollViewRef.current.scrollTop = scrollViewRef.current.scrollHeight;
    }
  };

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
