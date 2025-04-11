import React from "react";
import axios from "axios";
import styles from "./DateLabels.module.css";

// 부모 컴포넌트인 App.tsx에게 전달달
interface DateLabelsProps {
  onDateSelect: (
    messages: { id: number; text: string; sender: "user" | "bot" }[]
  ) => void;
}

const DateLabels: React.FC<DateLabelsProps> = ({ onDateSelect }) => {
  const dates = [
    "2025-03-28",
    "2025-03-27",
    "2025-03-26",
    "2025-03-25",
    "2025-03-24",
    "2025-03-23",
  ];

  // 클릭하면 서버로부터 과거 대화를 받아 message 배열로 전달
  const fetchHistory = async (date: string) => {
    try {
      const response = await axios.get(`http://localhost:8000/chat/history/${date}`);
      const history = response.data.history;

      if (history) {
        const formattedMessages = history.flatMap(
          (item: { question: string; answer: string }, index: number) => [
            { id: index * 2, text: item.question, sender: "user" },
            { id: index * 2 + 1, text: item.answer, sender: "bot" },
          ]
        );

        onDateSelect(formattedMessages);
      }
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  return (
    <div className={styles.labelContainer}>
      {dates.map((date, index) => (
        <button
          key={index}
          className={styles.labelButton}
          onClick={() => fetchHistory(date)}
        >
          {date}
        </button>
      ))}
    </div>
  );
};

export default DateLabels;
