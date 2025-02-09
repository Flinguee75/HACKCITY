"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import Link from "next/link"

interface CelestialCardProps {
  id: string
  name: string
  type: string
  image: string
  isHovered: boolean
  onHover: () => void
  onLeave: () => void
}

const CelestialCard: React.FC<CelestialCardProps> = ({ id, name, type, image, isHovered, onHover, onLeave }) => {
  const [isFlipped, setIsFlipped] = useState(false)

  const handleClick = () => {
    setIsFlipped(!isFlipped)
  }

  return (
    <div
      className="relative w-full h-80 cursor-pointer perspective"
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
      onClick={handleClick}
    >
      <motion.div
        className="w-full h-full transition-all duration-500 preserve-3d"
        animate={{ rotateY: isFlipped ? 180 : 0 }}
      >
        <div className="absolute w-full h-full backface-hidden">
          <img src={image || "/placeholder.svg"} alt={name} className="w-full h-full object-cover rounded-lg" />
          <div className="absolute inset-0 bg-gradient-to-t from-space-dark to-transparent rounded-lg" />
          <div className="absolute bottom-4 left-4">
            <h3 className="text-2xl font-bold">{name}</h3>
            <p className="text-glow-blue">{type}</p>
          </div>
          {isHovered && (
            <motion.div
              className="absolute inset-0 border-2 border-glow-blue rounded-lg"
              initial={{ opacity: 0, scale: 1.1 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
            />
          )}
        </div>
        <div className="absolute w-full h-full backface-hidden bg-space-dark bg-opacity-90 rounded-lg flex flex-col justify-center items-center p-6 rotate-y-180">
          <h3 className="text-2xl font-bold mb-4">{name}</h3>
          <p className="text-center mb-6">Click to learn more about {name} and its unique characteristics.</p>
          <Link
            href={`/celestial/${id}`}
            className="bg-glow-blue text-space-dark px-6 py-2 rounded-full font-semibold hover:bg-blue-400 transition-colors"
          >
            View Details
          </Link>
        </div>
      </motion.div>
    </div>
  )
}

export default CelestialCard

