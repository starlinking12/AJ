import React from 'react';
import './ChatSurface.css';
const ChatSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="chat-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <div className="chat-messages">
            {(data?.messages || []).map((m: any, i: number) => (
                <div key={i} className={`chat-bubble ${m.role}`}>{m.content}</div>
            ))}
        </div>
    </div>
);
export default ChatSurface;