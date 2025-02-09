import { exec } from 'child_process';
import { NextResponse } from 'next/server';
import path from 'path';

export async function POST() {
    try {
        const serverPath = path.join(process.cwd(), 'backend', 'start_server.py');
        exec(`python ${serverPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Erreur: ${error}`);
                return;
            }
            console.log(`Sortie: ${stdout}`);
        });

        return NextResponse.json({ status: 'started' });
    } catch (error) {
        console.error('Erreur lors du démarrage du serveur:', error);
        return NextResponse.json({ status: 'error', message: error.message }, { status: 500 });
    }
} 