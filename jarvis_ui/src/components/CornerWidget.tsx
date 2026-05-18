import React from 'react';
import CornerMinimized from './CornerMinimized';
import CornerMaximized from './CornerMaximized';
import './CornerWidget.css';

interface CornerWidgetProps {
    minimized?: boolean;
    onClick?: () => void;
}

const CornerWidget: React.FC<CornerWidgetProps> = ({
    minimized = true,
    onClick
}) => {
    return (
        <div className="corner-widget" onClick={onClick}>
            {minimized ? <CornerMinimized /> : <CornerMaximized />}
        </div>
    );
};

export default CornerWidget;