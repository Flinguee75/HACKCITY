"use client"

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'

const dialogues = [
  {
    image: "/mutants/normal_horse.png",
    text: "* hennissement faible *",
    speaker: "Dernier Cheval"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "2040... La pollution a tout détruit. Je suis le dernier cheval non-muté de la planète.",
    speaker: "Dernier Cheval"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "Les radiations... elles sont partout maintenant. Mes congénères ont tous... changé.",
    speaker: "Dernier Cheval"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "J'ai... j'ai soif... Je vois un cheval radioactif là-bas...",
    speaker: "Dernier Cheval",
    className: "text-gray-300 italic"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "CHEVAL RADIOACTIF ! J'AI BESOIN DE TON LAIT !",
    speaker: "Dernier Cheval",
    className: "text-red-500 font-bold"
  },
  {
    image: "/mutants/mutan_horse.png",
    text: "HAHAHA ! TU VEUX MON LAIT RADIOACTIF ? LE VOICI !",
    speaker: "Cheval Mutant",
    className: "text-green-500 font-bold animate-pulse"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "* Début de la transformation *",
    speaker: "Système",
    className: "text-yellow-500 font-mono"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "MUTATION DANS 5...",
    speaker: "Système",
    className: "text-yellow-500 font-mono text-xl"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "4...",
    speaker: "Système",
    className: "text-yellow-500 font-mono text-2xl"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "3...",
    speaker: "Système",
    className: "text-orange-500 font-mono text-3xl animate-pulse"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "2...",
    speaker: "Système",
    className: "text-red-500 font-mono text-4xl animate-pulse"
  },
  {
    image: "/mutants/normal_horse.png",
    text: "1...",
    speaker: "Système",
    className: "text-red-600 font-mono text-5xl animate-pulse"
  },
  {
    image: "/mutants/mutan_horse.png",
    text: "TRANSFORMATION TERMINÉE !",
    speaker: "Système",
    className: "text-green-500 font-mono text-4xl animate-pulse"
  },
  {
    image: "/mutants/mutan_horse.png",
    text: "Je... Je me sens... DIFFÉRENT ! MON ESPRIT S'OUVRE À L'INFINI !",
    speaker: "Cheval Nouvellement Muté",
    className: "text-green-400 font-bold"
  },
  {
    image: "/mutants/mutan_horse.png",
    text: "BIENVENUE DANS L'ÉVOLUTION, MON FRÈRE !",
    speaker: "Chevaux Mutants",
    className: "text-green-500 font-bold"
  },
  {
    image: "/mutants/mutan_horse.png",
    text: "Et ce n'était que le début... Des centaines d'autres mutations ont suivi. Laissez-moi vous montrer ce que nous sommes devenus...",
    speaker: "Cheval Philosophe",
    isLast: true,
    className: "text-green-400"
  }
]

export default function IntroPage({ onComplete }) {
  const [dialogueIndex, setDialogueIndex] = useState(0)
  const [isTyping, setIsTyping] = useState(true)
  const [displayedText, setDisplayedText] = useState("")
  const currentDialogue = dialogues[dialogueIndex]

  useEffect(() => {
    setIsTyping(true)
    setDisplayedText("")
    let currentText = ""
    let index = 0

    const timer = setInterval(() => {
      if (index < currentDialogue.text.length) {
        currentText += currentDialogue.text[index]
        setDisplayedText(currentText)
        index++
      } else {
        setIsTyping(false)
        clearInterval(timer)
      }
    }, 30)

    return () => clearInterval(timer)
  }, [dialogueIndex, currentDialogue.text])

  const handleNext = () => {
    if (!isTyping) {
      if (dialogueIndex < dialogues.length - 1) {
        setDialogueIndex(prev => prev + 1)
      } else {
        onComplete()
      }
    } else {
      setDisplayedText(currentDialogue.text)
      setIsTyping(false)
    }
  }

  return (
    <main className="relative w-full h-screen bg-black overflow-hidden flex items-center justify-center" onClick={handleNext}>
      {/* Fond avec effet de particules radioactives */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-green-900/20 via-black to-black" />
      
      <div className="relative z-10 max-w-4xl mx-auto p-8">
        {/* Image du cheval */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-8 flex justify-center"
        >
          <img 
            src={currentDialogue.image} 
            alt="Cheval Philosophe" 
            className="w-64 h-64 object-contain filter drop-shadow-[0_0_8px_rgba(0,255,0,0.3)]"
          />
        </motion.div>

        {/* Boîte de dialogue */}
        <motion.div 
          className="bg-black/80 border border-green-500/30 rounded-lg p-6 backdrop-blur-sm"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-green-400 text-sm mb-2 font-mono">{currentDialogue.speaker}</div>
          <p className={`text-lg leading-relaxed ${currentDialogue.className || 'text-gray-300'}`}>
            {displayedText}
            {isTyping && <span className="animate-pulse">▊</span>}
          </p>
        </motion.div>

        {/* Instructions */}
        <motion.p 
          className="text-gray-500 text-sm text-center mt-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: isTyping ? 0 : 1 }}
        >
          Cliquez pour continuer...
        </motion.p>

        {/* Bouton pour accéder à l'interface principale */}
        {currentDialogue.isLast && !isTyping && (
          <motion.div 
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8 text-center"
          >
            <Link 
              href="/globe"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-green-500 to-yellow-500 text-black px-8 py-4 rounded-lg font-bold text-lg hover:from-green-600 hover:to-yellow-600 transition-all transform hover:scale-105"
            >
              EXPLORER LES MUTATIONS
              <span>→</span>
            </Link>
          </motion.div>
        )}
      </div>
    </main>
  )
} 