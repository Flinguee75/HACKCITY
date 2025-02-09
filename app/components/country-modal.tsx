"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/app/ui/dialog"
import { Button } from "@/app/ui/button"
import { Play } from "lucide-react"
import Image from "next/image"

interface CountryModalProps {
  isOpen: boolean
  onClose: () => void
  country: {
    country: string
    description: string
    imageUrl: string
  } | null
}

export function CountryModal({ isOpen, onClose, country }: CountryModalProps) {
  if (!country) return null

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">{country.country}</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4">
          <div className="relative aspect-video">
            <Image
              src={country.imageUrl || "/placeholder.svg"}
              alt={country.country}
              fill
              className="object-cover rounded-lg"
            />
          </div>
          <p className="text-muted-foreground">{country.description}</p>
          <Button className="w-full">
            <Play className="mr-2 h-4 w-4" />
            Learn More
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}

