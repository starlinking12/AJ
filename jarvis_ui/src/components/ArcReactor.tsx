import React from 'react';
import ArcReactorIdle from './ArcReactorIdle';
import ArcReactorListening from './ArcReactorListening';
import ArcReactorThinking from './ArcReactorThinking';
import ArcReactorSpeaking from './ArcReactorSpeaking';
import ArcReactorError from './ArcReactorError';
import './ArcReactor.css';

interface ArcReactorProps {
    voiceState: 'sleeping' | 'listening' | 'thinking' | 'speaking' | 'error';
}

const ArcReactor: React.FC<ArcReactorProps> = ({ voiceState }) => {
    const renderState = () => {
        switch (voiceState) {
            case 'sleeping':
                return <ArcReactorIdle />;
            case 'listening':
                return <ArcReactorListening />;
            case 'thinking':
                return <ArcReactorThinking />;
            case 'speaking':
                return <ArcReactorSpeaking />;
            case 'error':
                return <ArcReactorError />;
            default:
                return <ArcReactorIdle />;
        }
    };

    return (
        <div className="arc-reactor-wrapper">
            <div className="arc-reactor-container">
                {renderState()}
            </div>
        </div>
    );
};

export default ArcReactor;