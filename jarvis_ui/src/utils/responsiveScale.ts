export function getResponsiveScale(baseSize: number = 320): number {
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;
    const minDimension = Math.min(screenWidth, screenHeight);
    return Math.min(1, (minDimension * 0.4) / baseSize);
}

export function getArcReactorSize(): number {
    return Math.round(320 * getResponsiveScale());
}