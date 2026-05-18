type UIState = {
    arcReactorState: 'sleeping' | 'listening' | 'thinking' | 'speaking' | 'error';
    isMinimized: boolean;
    activeTask: string | null;
    showCommandPrompt: boolean;
};

export const uiStore: UIState = {
    arcReactorState: 'sleeping',
    isMinimized: false,
    activeTask: null,
    showCommandPrompt: false,
};