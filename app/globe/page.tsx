"use client"

import dynamic from "next/dynamic"
import { Suspense } from "react"
import Stars from "../components/stars"
import "../globals.css"

const GlobeComponent = dynamic(() => import("../components/globe"), { ssr: false })

export default function GlobePage() {
  return (
    <main className="relative w-full h-screen overflow-hidden bg-black flex flex-col items-center justify-center">
      <div className="fixed inset-0 z-0">
        <Stars />
      </div>
      <div className="w-[2400px] h-[1600px] z-10 relative">
        <div className="absolute inset-0 bg-black/50 z-0" />
        <Suspense fallback={<div className="text-white">Loading...</div>}>
          <GlobeComponent />
        </Suspense>
      </div>
    </main>
  )
} 