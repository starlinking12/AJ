import React from 'react';

interface PulseRingProps {
    count?: number;
    color?: string;
    speed?: number;
}

const PulseRing: React.FC<PulseRingProps> = ({
    count = 6,
    color = 'var(--arc-reactor-blue)',
    speed = 1
}) => {
    const rings = Array.from({ length: count }, (_, i) => {
        const size = 100 - (i * (60 / count));
        const opacity = 0.15 + (i * (0.35 / count));
        return (
            <div
                key={i}
                className="pulse-ring"
                style={{
                    width: `${size}%`,
                    height: `${size}%`,
                    borderColor: color,
                    opacity: opacity,
                    animationDuration: `${3.8 / speed}s`,
                    animationDelay: `${i * 0.1}s`,
                }}
            />
        );
    });

    return <div className="pulse-rings-container">{rings}</div>;
};

export default PulseRing;