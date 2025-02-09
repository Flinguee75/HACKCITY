import { exec } from 'child_process';
import { NextResponse } from 'next/server';
import path from 'path';

export async function POST(request: Request) {
    try {
        const { gameType } = await request.json();
        const projectRoot = process.cwd();
        const pythonScript = path.join(projectRoot, 'backend', 'game', `${gameType}_game.py`);
        
        // Lancer simplement avec 'start' sur Windows
        const command = `start python "${pythonScript}"`;
        
        exec(command, {
            cwd: path.join(projectRoot, 'backend', 'game')
        });

        return NextResponse.json({ status: 'started' });
    } catch (error) {
        console.error('Erreur:', error);
        return NextResponse.json({ status: 'error' }, { status: 500 });
    }
} 