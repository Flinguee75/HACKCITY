import { motion } from "framer-motion"
import type React from "react" // Added import for React

interface CardProps {
  children: React.ReactNode
  isFlipped: boolean
  onClick: () => void
}

export default function Card({ children, isFlipped, onClick }: CardProps) {
  return (
    <div className="card relative w-64 h-64 cursor-pointer" onClick={onClick}>
      <motion.div
        className="w-full h-full"
        initial={false}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, ease: "easeInOut" }}
        style={{ transformStyle: "preserve-3d" }}
      >
        <div className="absolute w-full h-full bg-white rounded-lg shadow-lg backface-hidden" />
        <div
          className="absolute w-full h-full bg-gray-800 rounded-lg shadow-lg flex items-center justify-center backface-hidden"
          style={{ transform: "rotateY(180deg)" }}
        >
          {children}
        </div>
      </motion.div>
    </div>
  )
}

