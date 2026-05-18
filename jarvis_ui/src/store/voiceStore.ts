type VoiceState = {
    isListening: boolean;
    isSpeaking: boolean;
    isProcessing: boolean;
    lastCommand: string;
    lastResponse: string;
};

export const voiceStore: VoiceState = {
    isListening: false,
    isSpeaking: false,
    isProcessing: false,
    lastCommand: '',
    lastResponse: '',
};