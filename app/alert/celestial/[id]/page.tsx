"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { motion } from "framer-motion"
import { Canvas } from "@react-three/fiber"
import { OrbitControls, Stars } from "@react-three/drei"
import CelestialBody3D from "../../components/CelestialBody3D"

interface CelestialBodyData {
  id: string
  name: string
  type: string
  mass: string
  radius: string
  orbitalPeriod: string
  atmosphere: string
  funFact: string
}

const CelestialBodyPage = () => {
  const { id } = useParams()
  const [bodyData, setBodyData] = useState<CelestialBodyData | null>(null)

  useEffect(() => {
    // In a real application, you would fetch this data from an API
    const fetchData = async () => {
      // Simulating API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      setBodyData({
        id: id as string,
        name: id as string,
        type: "Planet",
        mass: "5.97 × 10^24 kg",
        radius: "6,371 km",
        orbitalPeriod: "365.26 days",
        atmosphere: "Nitrogen, Oxygen, Argon",
        funFact: "Earth is the only known planet to support life.",
      })
    }
    fetchData()
  }, [id])

  if (!bodyData) {
    return <div className="h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <div className="min-h-screen pt-16">
      <motion.h1
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-4xl font-bold text-center mb-8 text-glow-blue"
      >
        {bodyData.name}
      </motion.h1>
      <div className="flex flex-col lg:flex-row">
        <div className="lg:w-1/2 h-[50vh] lg:h-[80vh]">
          <Canvas>
            <ambientLight intensity={0.5} />
            <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
            <CelestialBody3D />
            <OrbitControls />
            <Stars />
          </Canvas>
        </div>
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:w-1/2 p-8"
        >
          <h2 className="text-2xl font-semibold mb-4">Details</h2>
          <ul className="space-y-2">
            <li>
              <strong>Type:</strong> {bodyData.type}
            </li>
            <li>
              <strong>Mass:</strong> {bodyData.mass}
            </li>
            <li>
              <strong>Radius:</strong> {bodyData.radius}
            </li>
            <li>
              <strong>Orbital Period:</strong> {bodyData.orbitalPeriod}
            </li>
            <li>
              <strong>Atmosphere:</strong> {bodyData.atmosphere}
            </li>
          </ul>
          <h3 className="text-xl font-semibold mt-6 mb-2">Fun Fact</h3>
          <p>{bodyData.funFact}</p>
        </motion.div>
      </div>
    </div>
  )
}

export default CelestialBodyPage

