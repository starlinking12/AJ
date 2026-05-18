export class AudioVisualizer {
    private analyser: AnalyserNode | null = null;
    private dataArray: Uint8Array = new Uint8Array(128);

    async initialize(stream: MediaStream): Promise<boolean> {
        try {
            const audioCtx = new AudioContext();
            const source = audioCtx.createMediaStreamSource(stream);
            this.analyser = audioCtx.createAnalyser();
            this.analyser.fftSize = 256;
            source.connect(this.analyser);
            return true;
        } catch { return false; }
    }

    getFrequencyData(): Uint8Array {
        if (this.analyser) {
            this.analyser.getByteFrequencyData(this.dataArray);
        }
        return this.dataArray;
    }
}