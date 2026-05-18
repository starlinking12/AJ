import { useState, useCallback } from 'react';
export function useTransition() {
    const [transitioning, setTransitioning] = useState(false);
    const startTransition = useCallback(() => { setTransitioning(true); setTimeout(() => setTransitioning(false), 500); }, []);
    return { transitioning, startTransition };
}