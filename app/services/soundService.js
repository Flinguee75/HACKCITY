import { Howl } from 'howler';

const sounds = {
    background: new Howl({
        src: ['/sounds/background.mp3'], // Assurez-vous que le chemin est correct
        loop: true,
        volume: 0.5,
    }),
    splash: new Howl({
        src: ['/sounds/splash.mp3'],
        volume: 1.0,
    }),
    neigh: new Howl({
        src: ['/sounds/neigh.mp3'],
        volume: 1.0,
    }),
    punch: new Howl({
        src: ['/sounds/punch.mp3'],
        volume: 1.0,
    }),
    gameOver: new Howl({
        src: ['/sounds/gameover.mp3'],
        volume: 1.0,
    }),
    win: new Howl({
        src: ['/sounds/gamewin.mp3'],
        volume: 1.0,
    }),
};

export const playSound = (sound) => {
    if (sounds[sound]) {
        sounds[sound].play();
    }
};

export const stopSound = (sound) => {
    if (sounds[sound]) {
        sounds[sound].stop();
    }
};

export const playBackgroundMusic = () => {
    sounds.background.play();
};

export const stopBackgroundMusic = () => {
    sounds.background.stop();
}; 