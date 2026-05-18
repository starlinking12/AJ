import React, { useState, useEffect } from 'react';
import './CommandPrompt.css';

const CommandPrompt: React.FC<{text?: string}> = ({ text = 'Listening...' }) => {
    const [visible, setVisible] = useState(false);
    useEffect(() => { setVisible(true); return () => setVisible(false); }, [text]);
    return <div className={`command-prompt ${visible ? 'visible' : ''}`}>{text}</div>;
};
export default CommandPrompt;