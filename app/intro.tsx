"use client"

import { useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import BackgroundMusic from './components/BackgroundMusic.tsx'

export default function Intro() {
  const [isReady, setIsReady] = useState(false)

  return (
    <main className="relative w-full h-screen bg-black overflow-hidden flex items-center justify-center">
      {/* Fond avec effet de particules radioactives */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-green-900/20 via-black to-black" />
      
      <div className="relative z-10 max-w-4xl mx-auto p-8">
        <BackgroundMusic onReady={() => setIsReady(true)} />
        {/* Logo ou Titre */}
        <motion.h1 
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-7xl font-black text-center mb-12"
        >
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-green-400 via-yellow-400 to-red-500">
            MUTATION JEU
          </span>
          <div className="h-1 w-48 mx-auto bg-gradient-to-r from-green-400 via-yellow-400 to-red-500 rounded-full mt-4"></div>
        </motion.h1>

        {/* Texte d'introduction */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="space-y-6 text-gray-300 text-lg leading-relaxed"
        >
          <p className="text-2xl font-bold text-yellow-400 mb-8">
            ⚠️ RAPPORT CONFIDENTIEL - 2040 ⚠️
          </p>

          <p>
            En cette année 2040, notre monde a radicalement changé. Les déchets radioactifs et la pollution massive ont provoqué des mutations extraordinaires chez certaines espèces animales, leur conférant des capacités qui dépassent l'entendement.
          </p>

          <p>
            Trois cas majeurs ont été documentés et sont maintenant sous surveillance constante :
          </p>

          <ul className="space-y-4 ml-6 list-disc">
            <li className="text-red-400">
              Le Gorille Dimensionnel, capable d'altérer la réalité elle-même
            </li>
            <li className="text-green-400">
              Le Cheval Philosophe, dont l'intelligence dépasse celle de tous les superordinateurs combinés
            </li>
            <li className="text-blue-400">
              La Baleine Psychique, qui peut influencer les émotions à l'échelle continentale
            </li>
          </ul>

          <p className="italic text-gray-400 mt-8">
            Cette interface vous permettra d'explorer et d'étudier ces mutations extraordinaires. Soyez vigilant : ces créatures ont développé une conscience qui dépasse notre compréhension.
          </p>
        </motion.div>

        {/* Bouton pour accéder à l'interface principale */}
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
          className="mt-12 text-center"
        >
          <Link 
            href="/globe"
            className="inline-flex items-center gap-2 bg-gradient-to-r from-green-500 to-yellow-500 text-black px-8 py-4 rounded-lg font-bold text-lg hover:from-green-600 hover:to-yellow-600 transition-all transform hover:scale-105"
          >
            ACCÉDER À L'INTERFACE
            <span>→</span>
          </Link>
        </motion.div>

        {/* Badge classifié */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
          <p className="text-xs text-yellow-500/60 font-mono">
            NIVEAU D'ACCRÉDITATION REQUIS : MAXIMUM
          </p>
        </div>
      </div>
    </main>
  )
} 