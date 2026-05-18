import { useState, useEffect } from 'react';
export function useSystemMetrics() {
    const [metrics, setMetrics] = useState({ cpu: 0, ram: 0, gpu: 0 });
    useEffect(() => {
        const interval = setInterval(() => {
            setMetrics({ cpu: Math.random() * 100, ram: Math.random() * 100, gpu: Math.random() * 100 });
        }, 2000);
        return () => clearInterval(interval);
    }, []);
    return metrics;
}