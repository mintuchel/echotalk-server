import React, { useState, useRef } from "react";
import axios from "axios";
import styles from "./ChatbotUI.module.css";

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
}

const ChatbotUI: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const scrollViewRef = useRef<HTMLDivElement>(null);

  async function processUserQuery(prompt: string) {
    try {
      const API_URL = "http://localhost:8000/ask";

      const questionRequest = { prompt };

      const response = await axios.post(API_URL, questionRequest);

      const answerResponse = response.data;

      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: answerResponse.created_at,
          text: answerResponse.response,
          sender: "bot",
        },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  }

  // 사용자가 Send 버튼을 눌렀을때 또는 Enter 키를 눌렀을때 실행됨
  // 사용자의 입력 메시지를 저장하고 UI에 추가
  const handleSendMessage = async () => {
    // 빈 입력 시 아무 동작 안함
    if (inputMessage.trim() === "") return;

    const userQuery: Message = {
      id: Date.now(),
      text: inputMessage.trim(),
      sender: "user",
    };

    // userQuery 객체를 생성해서 입력된 메시지를 "user" 형태로 저장장
    setMessages((prevMessages) => [...prevMessages, userQuery]);

    // 입력창 초기화
    setInputMessage("");

    // processUserQuery 메서드를 사용해서 서버로 요청
    // 서버에서 응답을 받으면 BOT의 메시지가 UI에 추가됨됨
    await processUserQuery(inputMessage);

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
