export class AnimationEngine {
    private animations: Map<string, Animation> = new Map();

    create(name: string, keyframes: Keyframe[], options: KeyframeAnimationOptions): Animation {
        const el = document.createElement('div');
        const anim = el.animate(keyframes, options);
        this.animations.set(name, anim);
        return anim;
    }

    play(name: string) {
        this.animations.get(name)?.play();
    }

    pause(name: string) {
        this.animations.get(name)?.pause();
    }

    cancel(name: string) {
        this.animations.get(name)?.cancel();
        this.animations.delete(name);
    }
}