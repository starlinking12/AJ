import React from 'react';
import './CodeSurface.css';
const CodeSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="code-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <pre className="code-block">{data?.code || '// No code to display'}</pre>
    </div>
);
export default CodeSurface;