import React from "react";
import styles from "./DateLabels.module.css";

const DateLabels: React.FC = () => {
  const dates = ["2025-03-26", "2025-03-25", "2025-03-24"];

  return (
    <div className={styles.labelContainer}>
      {dates.map((date, index) => (
        <button key={index} className={styles.labelButton}>
          {date}
        </button>
      ))}
    </div>
  );
};

export default DateLabels;
