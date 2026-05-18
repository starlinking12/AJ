import { useState, useEffect } from 'react';
export function useVoiceState(): 'sleeping' | 'listening' | 'thinking' | 'speaking' | 'error' {
    const [state, setState] = useState<'sleeping' | 'listening' | 'thinking' | 'speaking' | 'error'>('sleeping');
    useEffect(() => {
        const handler = (e: CustomEvent) => setState(e.detail);
        window.addEventListener('jarvis-voice-state', handler as EventListener);
        return () => window.removeEventListener('jarvis-voice-state', handler as EventListener);
    }, []);
    return state;
}