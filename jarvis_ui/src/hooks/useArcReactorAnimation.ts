import { useState, useEffect } from 'react';
export function useArcReactorAnimation() {
    const [animationState, setAnimationState] = useState('idle');
    const transition = (newState: string) => setAnimationState(newState);
    return { animationState, transition };
}