import React, { useState, useCallback } from "react";
import styles from "../../../styles/ProgressBar.module.css";
import SliderHandle from './SliderHandle'; // Import the SliderHandle component

const ProgressBar = ({ percentage, className, onChangePercentage, interactable }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseDown = () => {
    if (!interactable) return;
    setIsDragging(true);
  };

  const handleMouseUp = () => {
    if (!interactable) return;
    setIsDragging(false);
  };

  const handleMouseMove = 
    (e) => {
      if (!isDragging || !interactable) return;
      const bar = e.currentTarget;
      const barRect = bar.getBoundingClientRect();
      const moveX = e.clientX - barRect.left;
      const newPercentage = Math.round((moveX / barRect.width) * 100);
      if (newPercentage >= 0 && newPercentage <= 100) onChangePercentage(newPercentage);
    };

  return (
    <div
      className={interactable ? styles.ProgressBarV2 + " " + className : styles.ProgressBar + " " + className}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseDown={handleMouseDown}
      onMouseLeave={handleMouseUp}
    >
      <div className={styles.ProgressDone} style={{ width: `${percentage}%` }} />
      <div 
        className={styles.SliderHandleContainer}
        style={{ left: `calc(${percentage}% - 15px)`, display: "block"}}
        >
        {interactable && <SliderHandle />}
      </div>
    </div>
  );
};

export default ProgressBar;
