import { Howl } from 'howler';
import { useEffect } from 'react';

const IntroSound = () => {
  useEffect(() => {
    const sound = new Howl({
      src: ['sounds/background.mp3'],
      autoplay: true,
      volume: 1.0,
      onplayerror: () => {

        console.log('Erreur de lecture du son');
        // Tentative de reprise de la lecture
        sound.once('unlock', () => {
          sound.play();
        });
      },
      onloaderror: (id, err) => {
        console.error('Erreur de chargement du son:', err);
      }
    });

    return () => {
      sound.unload();
    };
  }, []);

  return null;
};

export default IntroSound; 