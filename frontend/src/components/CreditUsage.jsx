"use client";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

export default function CreditUsage({ credits, total }) {
  const percentage = Math.max(0, Math.min(100, (credits / total) * 100));

  // Decide color based on percentage left
  let pathColor = "green";
  if (percentage <= 30) pathColor = "red";
  else if (percentage <= 60) pathColor = "yellow";

  return (
    <div className="w-10 h-10">
      <CircularProgressbar
        value={percentage}
        text={`${Math.floor(percentage)}%`}
        styles={buildStyles({
          textSize: "28px",
          pathColor,
          textColor: "#fff",
          trailColor: "#444",
        })}
      />
    </div>
  );
}
