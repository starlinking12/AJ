import React from 'react';
import './NewsSurface.css';
const NewsSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="news-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <h2 className="surface-title">News</h2>
        <div className="news-grid">
            {(data?.articles || []).map((a: any, i: number) => (
                <div key={i} className="news-card">
                    <div className="news-card-title">{a.title}</div>
                    <div className="news-card-source">{a.source}</div>
                    <div className="news-card-snippet">{a.snippet}</div>
                </div>
            ))}
        </div>
    </div>
);
export default NewsSurface;