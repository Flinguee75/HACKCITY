import { Progress } from "@/components/ui/progress"
import { useEffect, useState } from "react"
import { motion } from "framer-motion"

interface LoadingBarProps {
  onLoadingComplete: () => void;
}

export function LoadingBar({ onLoadingComplete }: LoadingBarProps) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const timer = setTimeout(() => {
      if (progress < 100) {
        setProgress(prev => {
          const newProgress = prev + 1
          if (newProgress === 100) {
            onLoadingComplete()
          }
          return newProgress
        })
      }
    }, 50) // Ajustez cette valeur pour modifier la vitesse de chargement

    return () => clearTimeout(timer)
  }, [progress, onLoadingComplete])

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 flex flex-col items-center justify-center bg-background"
    >
      <div className="w-[80%] max-w-[500px] space-y-4">
        <Progress value={progress} className="h-2" />
        <p className="text-center text-muted-foreground">
          Chargement... {progress}%
        </p>
      </div>
    </motion.div>
  )
} 