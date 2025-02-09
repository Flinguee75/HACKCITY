"use client"

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from "framer-motion"
import SpaceBackground from "./SpaceBackground"

interface IntroSequenceProps {
  onComplete: () => void
}

export default function IntroSequence({ onComplete }: IntroSequenceProps) {
  const [showStar, setShowStar] = useState(true)
  const [showHorse, setShowHorse] = useState(false)
  const [showDialog, setShowDialog] = useState(false)
  const [currentDialog, setCurrentDialog] = useState(0)
  const [currentText, setCurrentText] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [isExiting, setIsExiting] = useState(false)

  const dialogLines = [
    "Ha... Ha... Ha... Quelle vie de malade. Je suis né du sperme de mon père, et me voici complètement irradié.",
    "Je crois avoir la réponse... Les humains ont été trop gourmands, voulaient trop d'argent, voulaient trop devenir grands.",
    "En résumé... ils ne voulaient plus être lents. Ce n'était jamais suffisant, ils n'étaient jamais contents à 100%.",
    "Tout ce qui leur importait c'était l'argent, ils ne voulaient que faire des gros montants...",
    "En bref : argent, argent, argent = plus de parents non radioactifs.",
    "Mon père me répétait toujours une chose lorsqu'il me donnait son lait...",
    "'Bois, bois mon lait, fils. Dans 20-30 ans mon lait sera radioactif car les humains ont voulu devenir trop grands, trop peu lents.'",
    "Papa, papa, est-ce que je sais encore faire des additions ? Car le futur que tu prophétisais s'est révélé plus tôt que prévu : 5 ans dans le futur plutôt que 20.",
    "Comme quoi, vous, humains qui lisez ça, vous avez le pouvoir de changer... De tout changer, d'empêcher le monde de devenir un dépotoir radioactif.",
    "Première étape : recyclez, recyclez vos objets, vos déchets.",
    "Deuxième étape : manifestez contre les méga-corporations qui produisent énormément de pollution.",
    "Troisième étape : prenez conscience de votre pouvoir dans ce processus.",
    "Moi, en tant que cheval, je vous le dis : si les chefs du monde, les multimilliardaires, continuent ainsi, ma famille et moi allons mourir de la radioactivité.",
    "PEACE... Il est encore temps d'agir."
  ]

  useEffect(() => {
    const timer1 = setTimeout(() => {
      setShowStar(false)
      setShowHorse(true)
    }, 2000)
    const timer2 = setTimeout(() => {
      setShowDialog(true)
    }, 3000)

    return () => {
      clearTimeout(timer1)
      clearTimeout(timer2)
    }
  }, [])

  useEffect(() => {
    if (showDialog && currentDialog < dialogLines.length) {
      setIsTyping(true)
      let index = 0
      const text = dialogLines[currentDialog]
      setCurrentText("")

      const interval = setInterval(() => {
        if (index < text.length) {
          setCurrentText(prev => prev + text[index])
          index++
        } else {
          setIsTyping(false)
          clearInterval(interval)
        }
      }, 30)

      return () => clearInterval(interval)
    }
  }, [showDialog, currentDialog])

  const handleClick = () => {
    if (isTyping) {
      // Si en train de taper, afficher tout le texte immédiatement
      setCurrentText(dialogLines[currentDialog])
      setIsTyping(false)
    } else if (currentDialog < dialogLines.length - 1) {
      // Passer au dialogue suivant
      setCurrentDialog(prev => prev + 1)
    } else {
      // Fin des dialogues
      setIsExiting(true)
      setTimeout(onComplete, 1000)
    }
  }

  return (
    <motion.div 
      className="fixed inset-0 flex items-center justify-center"
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <SpaceBackground />
      
      <div className="absolute inset-0 bg-black bg-opacity-60" />

      <motion.div 
        className="relative text-center max-w-[400px] z-10"
        animate={isExiting ? {
          scale: [1, 1.2, 0],
          opacity: [1, 1, 0],
          rotate: [0, 0, 180]
        } : {}}
        transition={{ duration: 1, ease: "easeInOut" }}
      >
        <AnimatePresence>
          {showStar && (
            <motion.div
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: [0, 1, 2], opacity: [0, 1, 0] }}
              exit={{ scale: 3, opacity: 0 }}
              transition={{ duration: 2 }}
              className="absolute inset-0 flex items-center justify-center"
            >
              <div className="star-shape w-16 h-16" />
            </motion.div>
          )}
        </AnimatePresence>

        {showHorse && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mb-4"
          >
            <img
              src="/mutants/mutan_horse.png"
              alt="Horse Spirit"
              style={{
                width: '200px',
                height: '200px',
                filter: 'drop-shadow(0 0 20px rgba(255,255,255,0.3))',
                margin: '0 auto'
              }}
            />
          </motion.div>
        )}

        {showDialog && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-[rgba(0,43,22,0.9)] backdrop-blur-sm p-4 rounded-lg border-2 border-[#7affb9] cursor-pointer hover:bg-[rgba(0,53,32,0.9)] transition-all hover:scale-105 mx-auto"
            onClick={handleClick}
          >
            <motion.p 
              key={currentDialog}
              className="text-[#e0fff4] text-lg mb-2 min-h-[4rem]"
            >
              {currentText}
            </motion.p>
            <span className="text-[#7affb9] text-xs animate-pulse">
              {isTyping ? "..." : isExiting ? "Préparation du voyage..." : "Cliquez pour continuer..."}
            </span>
          </motion.div>
        )}
      </motion.div>
    </motion.div>
  )
} 