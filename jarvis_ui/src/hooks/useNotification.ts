import { useCallback } from 'react';
export function useNotification() {
    const notify = useCallback((message: string) => {
        window.dispatchEvent(new CustomEvent('jarvis-notification', { detail: message }));
    }, []);
    return { notify };
}