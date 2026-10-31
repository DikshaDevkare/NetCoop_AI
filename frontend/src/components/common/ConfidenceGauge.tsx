import React from 'react';

interface ConfidenceGaugeProps {
  percentage: number;
  size?: number;
  strokeWidth?: number;
}

export const ConfidenceGauge: React.FC<ConfidenceGaugeProps> = ({
  percentage,
  size = 110,
  strokeWidth = 9,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const color = percentage >= 80 ? '#20E88A' : percentage >= 60 ? '#FFC247' : '#FF4568';

  return (
    <div className="relative flex flex-col items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#261d3b"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        {/* Animated Progress Arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          fill="transparent"
          style={{
            transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1)',
            filter: `drop-shadow(0 0 8px ${color}80)`
          }}
        />
      </svg>
      {/* Center Text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-xl font-extrabold text-white tracking-tight">{percentage}%</span>
        <span className="text-[9px] font-semibold text-[#A9A3B8] tracking-wider uppercase">Confidence</span>
      </div>
    </div>
  );
};
