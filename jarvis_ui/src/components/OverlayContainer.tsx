import React from 'react';
import './OverlayContainer.css';

interface OverlayContainerProps {
    children: React.ReactNode;
}

const OverlayContainer: React.FC<OverlayContainerProps> = ({ children }) => {
    return (
        <div className="overlay-container">
            {children}
        </div>
    );
};

export default OverlayContainer;