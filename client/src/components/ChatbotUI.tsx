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
      const response = await axios.post(import.meta.env.VITE_API_URL, {
        model_name: "phi",
        prompt: prompt,
      });

      const combinedResponse = response.data.response || "Please try again";

      setMessages((prevMessages) => [
        ...prevMessages,
        { id: Date.now(), text: combinedResponse, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  }

  const handleSendMessage = async () => {
    if (inputMessage.trim() === "") return;

    const userQuery: Message = {
      id: Date.now(),
      text: inputMessage.trim(),
      sender: "user",
    };
    setMessages((prevMessages) => [...prevMessages, userQuery]);
    setInputMessage("");
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
          placeholder="Type your message..."
          onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatbotUI;
