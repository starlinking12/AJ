import React from 'react';

interface ParticleFieldProps {
    count?: number;
    speed?: number;
    color?: string;
}

const ParticleField: React.FC<ParticleFieldProps> = ({
    count = 8,
    speed = 1,
    color = 'var(--arc-reactor-blue)'
}) => {
    const particles = Array.from({ length: count }, (_, i) => {
        const angle = (i / count) * 360;
        const distance = 40 + Math.random() * 20;
        const size = 1 + Math.random() * 2;
        return (
            <div
                key={i}
                className="particle"
                style={{
                    width: `${size}px`,
                    height: `${size}px`,
                    background: color,
                    top: `${50 + Math.sin(angle * Math.PI / 180) * distance}%`,
                    left: `${50 + Math.cos(angle * Math.PI / 180) * distance}%`,
                    animationDuration: `${5 / speed}s`,
                    animationDelay: `${i * 0.3}s`,
                }}
            />
        );
    });

    return <div className="particle-field">{particles}</div>;
};

export default ParticleField;