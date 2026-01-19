'use client';

import { useEffect, useState } from 'react';

interface ScoreCircleProps {
  score: number;
  size?: number;
}

export default function ScoreCircle({ score, size = 120 }: ScoreCircleProps) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const strokeWidth = size * 0.08;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedScore / 100) * circumference;

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedScore(score);
    }, 100);
    return () => clearTimeout(timer);
  }, [score]);

  const getColor = (s: number) => {
    if (s >= 80) return { stroke: '#22c55e', bg: '#dcfce7' };
    if (s >= 60) return { stroke: '#f59e0b', bg: '#fef3c7' };
    return { stroke: '#ef4444', bg: '#fee2e2' };
  };

  const colors = getColor(score);

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="transform -rotate-90"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth={strokeWidth}
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colors.stroke}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="score-circle"
          style={{
            transition: 'stroke-dashoffset 1s ease-out',
          }}
        />
      </svg>
      {/* Score text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className="font-bold"
          style={{
            fontSize: size * 0.3,
            color: colors.stroke,
          }}
        >
          {animatedScore}
        </span>
        <span
          className="text-gray-500"
          style={{ fontSize: size * 0.1 }}
        >
          / 100
        </span>
      </div>
    </div>
  );
}
