import React, { useState, useEffect } from "react";
import ChatbotUI from "./components/ChatbotUI";
import Header from "./components/Header";
import DateLabels from "./components/DateLabels";

const App: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [history, setHistory] = useState<
    { question: string; answer: string }[]
  >([]);

  useEffect(() => {
    if (selectedDate) {
      fetch(`http://localhost:8000/history/${selectedDate}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.history) {
            setHistory(data.history);
          }
        })
        .catch((error) => console.error("Error fetching history:", error));
    }
  }, [selectedDate]);

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
      <DateLabels onDateSelect={setSelectedDate} />
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
        {selectedDate && (
          <div
            style={{ marginTop: "20px", textAlign: "left", maxWidth: "600px" }}
          >
            <h3>📅 {selectedDate}의 기록</h3>
            {history.length > 0 ? (
              history.map((item, index) => (
                <div
                  key={index}
                  style={{
                    marginBottom: "10px",
                    padding: "10px",
                    border: "1px solid #ccc",
                    borderRadius: "5px",
                  }}
                >
                  <p>
                    <strong>Q:</strong> {item.question}
                  </p>
                  <p>
                    <strong>A:</strong> {item.answer}
                  </p>
                </div>
              ))
            ) : (
              <p>해당 날짜의 기록이 없습니다.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
