"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import CelestialCard from "./CelestialCard"

const celestialBodies = [
  { id: "sun", name: "Sun", type: "Star", image: "/images/sun.jpg" },
  { id: "mercury", name: "Mercury", type: "Planet", image: "/images/mercury.jpg" },
  { id: "venus", name: "Venus", type: "Planet", image: "/images/venus.jpg" },
  { id: "earth", name: "Earth", type: "Planet", image: "/images/earth.jpg" },
  { id: "mars", name: "Mars", type: "Planet", image: "/images/mars.jpg" },
  { id: "jupiter", name: "Jupiter", type: "Planet", image: "/images/jupiter.jpg" },
  { id: "saturn", name: "Saturn", type: "Planet", image: "/images/saturn.jpg" },
  { id: "uranus", name: "Uranus", type: "Planet", image: "/images/uranus.jpg" },
  { id: "neptune", name: "Neptune", type: "Planet", image: "/images/neptune.jpg" },
]

const CelestialCards = () => {
  const [hoveredCard, setHoveredCard] = useState<string | null>(null)

  return (
    <section id="celestial-cards" className="py-16 px-4">
      <h2 className="text-4xl font-bold text-center mb-12 text-glow-blue">Our Cosmic Neighborhood</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {celestialBodies.map((body) => (
          <motion.div
            key={body.id}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            whileHover={{ scale: 1.05 }}
          >
            <CelestialCard
              {...body}
              isHovered={hoveredCard === body.id}
              onHover={() => setHoveredCard(body.id)}
              onLeave={() => setHoveredCard(null)}
            />
          </motion.div>
        ))}
      </div>
    </section>
  )
}

export default CelestialCards

