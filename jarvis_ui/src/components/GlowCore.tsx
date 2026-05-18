import React from 'react';

interface GlowCoreProps {
    brightness?: number;
    pulse?: boolean;
    pulseSpeed?: number;
    color?: string;
}

const GlowCore: React.FC<GlowCoreProps> = ({
    brightness = 0.5,
    pulse = true,
    pulseSpeed = 1,
    color = 'var(--arc-reactor-blue)'
}) => {
    const coreStyle = {
        background: `radial-gradient(circle at 40% 35%,
            rgba(255, 255, 255, ${brightness}) 0%,
            rgba(220, 245, 255, ${brightness * 0.9}) 8%,
            rgba(0, 200, 240, ${brightness * 0.8}) 25%,
            rgba(0, 150, 220, ${brightness * 0.5}) 50%,
            rgba(0, 90, 180, ${brightness * 0.2}) 75%,
            rgba(0, 40, 120, 0.05) 100%)`,
        boxShadow: `
            0 0 ${35 * brightness}px ${color},
            0 0 ${90 * brightness}px ${color},
            0 0 ${160 * brightness}px ${color},
            0 0 ${250 * brightness}px ${color}`,
        animation: pulse ? `core-pulse ${3.8 / pulseSpeed}s ease-in-out infinite` : 'none',
    };

    return <div className="glow-core" style={coreStyle} />;
};

export default GlowCore;