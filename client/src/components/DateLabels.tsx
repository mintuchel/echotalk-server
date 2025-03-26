import React, { useState } from "react";
import styles from "./DateLabels.module.css";

const DateLabels: React.FC<{ onDateSelect: (date: string) => void }> = ({
  onDateSelect,
}) => {
  const dates = ["2024-03-26", "2024-03-25", "2024-03-24"];

  return (
    <div className={styles.labelContainer}>
      {dates.map((date, index) => (
        <button
          key={index}
          className={styles.labelButton}
          onClick={() => onDateSelect(date)}
        >
          {date}
        </button>
      ))}
    </div>
  );
};

export default DateLabels;
