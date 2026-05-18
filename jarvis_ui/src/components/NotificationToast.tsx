import React, { useState, useEffect } from 'react';
import './NotificationToast.css';
interface Toast { id: number; message: string; }
const NotificationToast: React.FC = () => {
    const [toasts, setToasts] = useState<Toast[]>([]);
    useEffect(() => {
        const handler = (e: CustomEvent) => {
            const id = Date.now();
            setToasts(prev => [...prev, { id, message: e.detail }]);
            setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
        };
        window.addEventListener('jarvis-notification', handler as EventListener);
        return () => window.removeEventListener('jarvis-notification', handler as EventListener);
    }, []);
    if (toasts.length === 0) return null;
    return (
        <div className="notification-container">
            {toasts.map(t => <div key={t.id} className="notification-toast">{t.message}</div>)}
        </div>
    );
};
export default NotificationToast;