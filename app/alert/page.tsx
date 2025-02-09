"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import SpaceBackground from "./components/SpaceBackground"
import FlipCard from "./components/FlipCard"
import Circle from "./components/shapes/Circle"
import Triangle from "./components/shapes/Triangle"
import Square from "./components/shapes/Square"
import IntroSequence from "./components/IntroSequence"
import { useRouter } from 'next/navigation'

export default function Home() {
  const [showCards, setShowCards] = useState(false)
  const [flippedCard, setFlippedCard] = useState<number | null>(null)
  const [expandedCard, setExpandedCard] = useState<number | null>(null)
  const router = useRouter()

  const cardContents = [
    {
      title: "Les Baleines",
      image: "/mutants/mutan_whale.png",
      content: {
        density: [
          "Il ne reste qu'environ 400 baleines noires de l'Atlantique Nord.",
          "La population de baleines bleues est estimée entre 10,000 et 25,000 individus, alors qu'elle était de 350,000 avant la chasse commerciale.",
          "Les baleines à bosse se rétablissent lentement avec environ 80,000 individus dans le monde."
        ],
        locations: [
          "Les principales menaces actuelles sont :",
          "• Les collisions avec les navires commerciaux",
          "• L'enchevêtrement dans les filets de pêche",
          "• La pollution sonore qui perturbe leur communication",
          "• Le réchauffement climatique qui affecte leurs sources de nourriture"
        ],
        dangers: [
          "Comment pouvons-nous agir à notre échelle ?",
          "• Réduire notre consommation de plastique qui finit dans les océans",
          "• Choisir des produits de la mer certifiés durables",
          "• Soutenir les organisations de conservation marine",
          "• Participer à des actions de nettoyage des plages",
          "• Sensibiliser notre entourage à la protection des océans",
          "• Utiliser des applications pour signaler les observations de baleines aux scientifiques"
        ]
      }
    },
    {
      title: "Les Gorilles",
      image: "/mutants/mutan_monkey.png",
      content: {
        density: [
          "Il ne reste qu'environ 1,000 gorilles de montagne dans le monde.",
          "La population de gorilles des plaines orientales est estimée à 3,800 individus.",
          "Les gorilles des plaines occidentales comptent environ 100,000 individus."
        ],
        locations: [
          "Les principales menaces sont :",
          "• La destruction de leur habitat pour l'agriculture",
          "• Le braconnage",
          "• Les maladies transmises par l'homme",
          "• Les conflits armés dans leurs zones d'habitat"
        ],
        dangers: [
          "Actions possibles à notre niveau :",
          "• Acheter du bois certifié durable pour préserver leur habitat",
          "• Recycler nos téléphones portables (contenant du coltan, minerai extrait de leur habitat)",
          "• Soutenir les programmes de conservation",
          "• Choisir des produits sans huile de palme",
          "• Parrainer un gorille via une organisation de conservation",
          "• Sensibiliser sur l'importance de leur préservation"
        ]
      }
    },
    {
      title: "Les Chevaux",
      image: "/mutants/mutan_horse.png",
      content: {
        density: [
          "Il ne reste que 2,000 chevaux de Przewalski à l'état sauvage.",
          "Les mustangs sauvages d'Amérique du Nord sont environ 86,000.",
          "Plusieurs races de chevaux traditionnelles sont en danger critique d'extinction."
        ],
        locations: [
          "Les menaces principales incluent :",
          "• La perte d'habitat naturel",
          "• La compétition avec le bétail domestique",
          "• Les changements climatiques affectant leurs territoires",
          "• L'isolement génétique des populations"
        ],
        dangers: [
          "Comment contribuer à leur protection :",
          "• Soutenir les sanctuaires de chevaux sauvages",
          "• S'opposer aux projets de développement dans leurs territoires",
          "• Participer à des programmes de conservation",
          "• Sensibiliser sur l'importance des chevaux sauvages dans l'écosystème",
          "• Soutenir les initiatives de protection des prairies naturelles",
          "• Adopter ou parrainer un cheval sauvage via des organisations spécialisées"
        ]
      }
    }
  ]

  const handleCardClick = (index: number) => {
    if (expandedCard === index) {
      setExpandedCard(null)
      setFlippedCard(null)
    } else if (flippedCard === index) {
      setExpandedCard(index)
    } else {
      setFlippedCard(index)
    }
  }

  const handleOutsideClick = () => {
    if (expandedCard !== null) {
      setExpandedCard(null)
    }
    setFlippedCard(null)
  }

  const BackButton = () => (
    <button
      onClick={() => router.push('/globe')}
      className="fixed top-4 left-4 z-50 bg-black/50 p-2 rounded-full hover:bg-black/70 transition-colors"
    >
      ← Retour au Globe
    </button>
  )

  return (
    <>
      <BackButton />
      <AnimatePresence mode="wait">
        {!showCards ? (
          <IntroSequence onComplete={() => setShowCards(true)} />
        ) : (
          <motion.main
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="min-h-screen flex items-center justify-center relative overflow-hidden"
            onClick={handleOutsideClick}
          >
            <SpaceBackground />
            <div className="flex flex-col md:flex-row gap-8 z-10">
              <FlipCard
                isFlipped={flippedCard === 0}
                isExpanded={expandedCard === 0}
                onClick={(e) => {
                  e.stopPropagation()
                  handleCardClick(0)
                }}
                frontContent={
                  <img 
                    src="/mutants/icon/icon_whale.png"
                    alt="Icône baleine"
                    className="w-24 h-24 object-contain"
                  />
                }
                backContent="Les Baleines"
                scrollContent={cardContents[0]}
              />
              <FlipCard
                isFlipped={flippedCard === 1}
                isExpanded={expandedCard === 1}
                onClick={(e) => {
                  e.stopPropagation()
                  handleCardClick(1)
                }}
                frontContent={
                  <img 
                    src="/mutants/icon/icon_gorilla.png"
                    alt="Icône gorille"
                    className="w-24 h-24 object-contain"
                  />
                }
                backContent="Les Gorilles"
                scrollContent={cardContents[1]}
              />
              <FlipCard
                isFlipped={flippedCard === 2}
                isExpanded={expandedCard === 2}
                onClick={(e) => {
                  e.stopPropagation()
                  handleCardClick(2)
                }}
                frontContent={
                  <img 
                    src="/mutants/icon/icon_horse.png"
                    alt="Icône cheval"
                    className="w-24 h-24 object-contain"
                  />
                }
                backContent="Les Chevaux"
                scrollContent={cardContents[2]}
              />
            </div>
          </motion.main>
        )}
      </AnimatePresence>
    </>
  )
}

