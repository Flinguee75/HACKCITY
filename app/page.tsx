"use client"

import { useState } from "react"
import { AnimatePresence } from "framer-motion"
import { LoadingBar } from "@/components/LoadingBar"
import IntroSound from "@/components/IntroSound"
import IntroPage from './intro/page'
import { redirect } from "next/navigation"

export default function HomePage() {
  const [showIntro, setShowIntro] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [showGlobe, setShowGlobe] = useState(false)

  const handleIntroComplete = () => {
    setShowIntro(false)
    setIsLoading(true)
  }

  const handleLoadingComplete = () => {
    setIsLoading(false)
    setShowGlobe(true)
  }

  return (
    <div className="min-h-screen w-full bg-black">
      <AnimatePresence mode="wait">
        {showIntro && (
          <div className="w-full h-screen">
            <IntroSound />
            <IntroPage onComplete={handleIntroComplete} />
          </div>
        )}
        
        {isLoading && (
          <div className="w-full h-screen">
            <LoadingBar onLoadingComplete={handleLoadingComplete} />
          </div>
        )}
        
        {showGlobe && (
          <div className="w-full h-screen">
            {/* Votre composant Globe ici */}
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}

