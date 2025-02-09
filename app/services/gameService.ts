import { exec } from 'child_process';
import path from 'path';

export async function startGame(gameType: string) {
    try {
        const response = await fetch('/api/launch-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ gameType })
        });
        
        return await response.json();
    } catch (error) {
        console.error("Erreur dans startGame:", error);
        throw error;
    }
}

export async function getGameState() {
    const response = await fetch('http://localhost:8000/game-state');
    return response.json();
}

export async function updateMutation(location: string) {
    const response = await fetch(`http://localhost:8000/update-mutation/${location}`, {
        method: 'POST'
    });
    return response.json();
} 