import React from 'react';

const LoadingPage = () => {
    return (
        <div className="loading-container">
            <h1>Chargement...</h1>
            <p>Veuillez patienter pendant que nous préparons votre expérience.</p>
            {/* Vous pouvez ajouter une animation ou un spinner ici */}
            <style jsx>{`
                .loading-container {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #000; /* Couleur de fond */
                    color: #fff; /* Couleur du texte */
                }
            `}</style>
        </div>
    );
};

export default LoadingPage; 