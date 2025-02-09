import { useState, useEffect } from 'react';
import BackgroundMusic from './components/BackgroundMusic';
import LoadingPage from './components/LoadingPage';

export default function Layout({ children }) {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simuler un chargement de 2 secondes
        const timer = setTimeout(() => {
            setLoading(false);
        }, 2000); // Changez la durée selon vos besoins

        return () => clearTimeout(timer);
    }, []);

    return (
        <div>
            <BackgroundMusic />
            {loading ? <LoadingPage /> : children}
        </div>
    );
} 