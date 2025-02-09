"use client"

import { motion } from "framer-motion"

interface FlipCardProps {
  isFlipped: boolean
  isExpanded: boolean
  onClick: (e: React.MouseEvent) => void
  frontContent: React.ReactNode
  backContent: string
  scrollContent?: {
    title: string
    content: {
      density: string[]
      locations: string[]
      dangers: string[]
    }
    image?: string
  }
}

export default function FlipCard({
  isFlipped,
  isExpanded,
  onClick,
  frontContent,
  backContent,
  scrollContent
}: FlipCardProps) {
  return (
    <motion.div
      layout
      className={`flip-card ${isFlipped ? 'flipped' : ''}`}
      animate={isExpanded ? {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        x: 0,
        y: 0,
        zIndex: 50
      } : {
        position: 'relative',
        width: '300px',
        height: '400px',
        x: 0,
        y: 0
      }}
      transition={{ duration: 0.5, ease: "easeInOut" }}
      onClick={onClick}
    >
      <motion.div className="flip-card-inner">
        <div className="flip-card-front">
          {frontContent}
        </div>
        <div className="flip-card-back">
          {isExpanded ? (
            <div className="fixed inset-0 flex items-center justify-center bg-black/80">
              <motion.div 
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="parchment-scroll w-[95%] md:w-[80%] h-[90%] max-w-4xl mx-auto overflow-hidden"
              >
                <div className="parchment-content h-full overflow-y-auto p-8">
                  <h2 className="text-4xl font-serif mb-8 text-amber-800 text-center">
                    {scrollContent?.title}
                  </h2>
                  
                  {scrollContent?.image && (
                    <div className="mb-8 flex justify-center">
                      <img 
                        src={scrollContent.image} 
                        alt="Animal en danger"
                        className="rounded-lg shadow-lg max-w-full h-auto max-h-[300px] object-cover"
                        onError={(e) => {
                          e.currentTarget.src = '/fallback-image.png'
                        }}
                      />
                    </div>
                  )}

                  <div className="text-left space-y-8 px-4">
                    <section className="bg-[rgba(255,247,233,0.5)] p-6 rounded-lg">
                      <h3 className="text-2xl font-serif mb-6 text-amber-700 border-b border-amber-200 pb-2">
                        {/* Titre dynamique basé sur le type d'animal */}
                        {scrollContent?.title.includes("Baleines") ? "Densité des baleines" :
                         scrollContent?.title.includes("Gorilles") ? "Densité des gorilles" :
                         "Population des chevaux"}
                      </h3>
                      {scrollContent?.content.density.map((text, i) => (
                        <p key={i} className="mb-4 text-lg text-amber-900 leading-relaxed">
                          {text}
                        </p>
                      ))}
                    </section>
                    
                    <section className="bg-[rgba(255,247,233,0.5)] p-6 rounded-lg">
                      <h3 className="text-2xl font-serif mb-6 text-amber-700 border-b border-amber-200 pb-2">
                        Zones les plus touchées
                      </h3>
                      {scrollContent?.content.locations.map((text, i) => (
                        <p key={i} className="mb-4 text-lg text-amber-900 leading-relaxed">
                          {text}
                        </p>
                      ))}
                    </section>
                    
                    <section className="bg-[rgba(255,247,233,0.5)] p-6 rounded-lg">
                      <h3 className="text-2xl font-serif mb-6 text-amber-700 border-b border-amber-200 pb-2">
                        Menaces principales
                      </h3>
                      {scrollContent?.content.dangers.map((text, i) => (
                        <p key={i} className="mb-4 text-lg text-amber-900 leading-relaxed">
                          {text}
                        </p>
                      ))}
                    </section>
                  </div>
                </div>
              </motion.div>
            </div>
          ) : (
            <span>{backContent}</span>
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}

