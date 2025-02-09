"use client"

import { useState } from "react"
import { CountryModal } from "./country-modal"

interface Point {
  id: number
  x: number
  y: number
  country: string
  description: string
  imageUrl: string
}

const points: Point[] = [
  {
    id: 1,
    x: 25,
    y: 40,
    country: "United States",
    description: "Experience the diversity of landscapes and cultures across the United States.",
    imageUrl: "/placeholder.svg?height=200&width=300",
  },
  {
    id: 2,
    x: 82,
    y: 35,
    country: "Japan",
    description: "Discover the blend of ancient traditions and cutting-edge technology in Japan.",
    imageUrl: "/placeholder.svg?height=200&width=300",
  },
  {
    id: 3,
    x: 85,
    y: 75,
    country: "Australia",
    description: "Explore the unique wildlife and natural wonders of the Australian continent.",
    imageUrl: "/placeholder.svg?height=200&width=300",
  },
]

export default function WorldMap() {
  const [selectedPoint, setSelectedPoint] = useState<Point | null>(null)

  return (
    <div className="relative w-full max-w-4xl mx-auto">
      <svg viewBox="0 0 1000 500" className="w-full h-auto" style={{ background: "#87CEEB" }}>
        {/* Simplified world map */}
        <path
          d="M150,100 Q400,50 700,120 T900,150 V400 Q650,450 350,380 T100,350 V100"
          fill="#90EE90"
          stroke="#2E8B57"
          strokeWidth="2"
        />
        {/* You can add more path elements to represent continents or countries */}

        {points.map((point) => (
          <circle
            key={point.id}
            cx={`${point.x}%`}
            cy={`${point.y}%`}
            r="10"
            fill="red"
            className="cursor-pointer hover:fill-red-700 transition-colors"
            onClick={() => setSelectedPoint(point)}
          />
        ))}
      </svg>

      <CountryModal isOpen={!!selectedPoint} onClose={() => setSelectedPoint(null)} country={selectedPoint} />
    </div>
  )
}

