import React from 'react';

interface AudioWaveformProps {
    active?: boolean;
    barCount?: number;
    color?: string;
}

const AudioWaveform: React.FC<AudioWaveformProps> = ({
    active = false,
    barCount = 24,
    color = 'var(--arc-reactor-blue)'
}) => {
    const bars = Array.from({ length: barCount }, (_, i) => (
        <div
            key={i}
            className="waveform-bar"
            style={{
                background: color,
                animationDuration: active ? `${0.5 + Math.random() * 0.8}s` : '0s',
                animationDelay: `${i * 0.05}s`,
                height: active ? `${20 + Math.random() * 60}%` : '5%',
            }}
        />
    ));

    return (
        <div className="audio-waveform">
            {bars}
        </div>
    );
};

export default AudioWaveform;