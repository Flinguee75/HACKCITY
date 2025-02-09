"use client"

import { motion } from "framer-motion"

const HeroSection = () => {
  return (
    <section className="h-screen flex flex-col justify-center items-center text-center px-4">
      <motion.h1
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="text-5xl md:text-7xl font-bold mb-6 text-glow-blue"
      >
        Explore the Cosmos
      </motion.h1>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.5 }}
        className="text-xl md:text-2xl mb-8 max-w-2xl"
      >
        Embark on a journey through our solar system and beyond. Discover the wonders of space in stunning detail.
      </motion.p>
      <motion.button
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 1 }}
        className="bg-glow-blue text-space-dark px-8 py-3 rounded-full text-lg font-semibold hover:bg-blue-400 transition-colors"
        onClick={() => document.getElementById("celestial-cards")?.scrollIntoView({ behavior: "smooth" })}
      >
        Start Exploring
      </motion.button>
    </section>
  )
}

export default HeroSection

