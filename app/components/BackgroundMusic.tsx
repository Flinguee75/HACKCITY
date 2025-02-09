import { useEffect } from 'react';
import { Howl } from 'howler';

interface BackgroundMusicProps {
    onReady?: () => void; // Définir la prop onReady
}

const BackgroundMusic: React.FC<BackgroundMusicProps> = ({ onReady }) => {
    useEffect(() => {
        console.log("BackgroundMusic component mounted");
        const sound = new Howl({
            src: ['/sounds/background.mp3'], // Assurez-vous que le chemin est correct
            loop: true,
            volume: 1.0,
        });

        sound.play();

        if (onReady) {
            onReady(); // Appeler onReady lorsque la musique commence
        }

        return () => {
            sound.stop(); // Arrête la musique lorsque le composant est démonté
        };
    }, [onReady]);

    return null; // Ce composant ne rend rien
};

export default BackgroundMusic; 