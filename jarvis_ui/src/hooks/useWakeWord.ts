import { useState, useEffect } from 'react';
export function useWakeWord() {
    const [awake, setAwake] = useState(false);
    useEffect(() => {
        const handler = (e: CustomEvent) => setAwake(e.detail === 'awake');
        window.addEventListener('jarvis-wake-state', handler as EventListener);
        return () => window.removeEventListener('jarvis-wake-state', handler as EventListener);
    }, []);
    return awake;
}