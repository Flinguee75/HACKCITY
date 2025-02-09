"use client"

import { useRef, useState, useEffect } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { OrbitControls, Billboard } from "@react-three/drei"
import * as THREE from "three"
import { useLoader } from "@react-three/fiber"
import { startGame, getGameState, updateMutation } from '../services/gameService'
import dynamic from 'next/dynamic'
import BackgroundMusic from './BackgroundMusic'

const points = [
  {
    position: [0.5, 0.8, -0.5],
    name: "Forêt Amazonienne",
    description: "En 2040, la déforestation massive a exposé d'anciens sites d'extraction d'uranium, créant une zone de contamination inattendue.",
    crazyStory: "Les scientifiques ont découvert une nouvelle espèce de singes bioluminescents qui utilisent leur lueur radioactive pour communiquer la nuit. Ces 'Singes Lucioles' auraient développé la capacité de faire pousser des plantes en les touchant, créant des jardins phosphorescents dans la canopée.",
    imageUrl: "/mutants/mutan_monkey.png",
    iconUrl: "/mutants/icon/icon_gorilla.png",
    color: "red",
    buttonText: "QUI SERA LE PLUS FORT ?"
  },
  {
    position: [-0.8, -0.2, 0.8],
    name: "Forêt du Bassin du Congo", 
    description: "Une horde de chevaux mutants radioactifs s'est développée dans la région, leurs crinières brillant d'une lueur surnaturelle en 2040.",
    crazyStory: "Les chevaux ont développé une intelligence supérieure suite à leur exposition aux radiations. Leurs crinières émettent une lumière phosphorescente qui pulse au rythme de leurs pensées. Les scientifiques affirment qu'ils communiquent par ces signaux lumineux et résolvent des équations complexes.",
    imageUrl: "/mutants/mutan_horse.png",
    iconUrl: "/mutants/icon/icon_horse.png",
    color: "green",
    buttonText: "SAUVER LA FORÊT"
  },
  {
    position: [0.2, -0.6, -0.9],
    name: "Grande Zone de Déchets du Pacifique",

    description: "En 2040, les déchets nucléaires accumulés ont créé un vortex radioactif au cœur du gyre du Pacifique.",
    crazyStory: "Une colonie de méduses mutantes s'est développée, absorbant la radioactivité des déchets. Ces 'Méduses Atomiques' émettent des impulsions électromagnétiques qui perturbent les appareils électroniques, mais créent aussi un spectacle de lumière hypnotique visible depuis l'espace.",
    imageUrl: "/mutants/mutan_whale.png",
    iconUrl: "/mutants/icon/icon_whale.png",
    color: "blue",
    buttonText: "NETTOYER L'OCÉAN"
  },
]

function Satellite({ radius, speed, offset, color = "#c0c0c0", image = "/satellites/sat.png" }: { 
  radius: number, 
  speed: number, 
  offset: number,
  color?: string,
  image?: string
}) {
  const satelliteRef = useRef<THREE.Group>(null)
  const texture = useLoader(THREE.TextureLoader, image)

  useFrame((state) => {
    if (satelliteRef.current) {
      const time = state.clock.getElapsedTime()
      satelliteRef.current.position.x = Math.cos(time * speed + offset) * radius
      satelliteRef.current.position.z = Math.sin(time * speed + offset) * radius
      satelliteRef.current.position.y = Math.sin(time * speed * 0.5) * 0.2
      
      satelliteRef.current.rotation.y = time * speed * 0.5
    }
  })

  return (
    <group ref={satelliteRef}>
      <Billboard
        follow={true}
        lockX={false}
        lockY={false}
        lockZ={false}
      >
        <mesh>
          <planeGeometry args={[0.15, 0.15]} />
          <meshBasicMaterial 
            map={texture}
            transparent
            opacity={1}
            depthWrite={false}
          />
        </mesh>
      </Billboard>
    </group>
  )
}

function SpaceObject({ position, icon, color, scale = 1 }: {
  position: [number, number, number]
  icon: string
  color: string
  scale?: number
}) {
  const [hover, setHover] = useState(false)

  return (
    <Billboard
      follow={true}
      lockX={false}
      lockY={false}
      lockZ={false}
    >
      <group position={position}>
        <mesh
          onPointerEnter={() => setHover(true)}
          onPointerLeave={() => setHover(false)}
          scale={hover ? scale * 1.2 : scale}
        >
          <planeGeometry args={[0.3, 0.3]} />
          <meshBasicMaterial
            transparent
            opacity={0.8}
            color={color}
            depthWrite={false}
          >
            <texture attach="map" url={icon} />
          </meshBasicMaterial>
        </mesh>
      </group>
    </Billboard>
  )
}

function Comet() {
  const cometRef = useRef<THREE.Group>(null)
  const [isActive, setIsActive] = useState(false)
  const [startPosition, setStartPosition] = useState<[number, number, number]>([0, 0, 0])
  const [endPosition, setEndPosition] = useState<[number, number, number]>([0, 0, 0])
  const speed = 0.8

  useEffect(() => {
    const spawnComet = () => {
      const side = Math.floor(Math.random() * 2)
      let start: [number, number, number]
      let end: [number, number, number]
      const height = (Math.random() - 0.5) * 0.8
      const depth = (Math.random() - 0.5) * 2

      if (side === 0) {
        start = [-3, height, depth]
        end = [3, height, depth]
      } else {
        start = [3, height, depth]
        end = [-3, height, depth]
      }

      setStartPosition(start)
      setEndPosition(end)
      setIsActive(true)

      setTimeout(() => {
        setIsActive(false)
      }, 6000)
    }

    const interval = setInterval(() => {
      if (!isActive) {
        spawnComet()
      }
    }, 30000)

    return () => clearInterval(interval)
  }, [isActive])

  useFrame((state) => {
    if (cometRef.current && isActive) {
      const time = state.clock.getElapsedTime() * speed
      const progress = (time % 8) / 8

      cometRef.current.position.x = startPosition[0] + (endPosition[0] - startPosition[0]) * progress
      cometRef.current.position.y = startPosition[1]
      cometRef.current.position.z = startPosition[2]
    }
  })

  if (!isActive) return null

  return (
    <group ref={cometRef}>
      <mesh>
        <sphereGeometry args={[0.03, 16, 16]} />
        <meshBasicMaterial color="#ff6600" />
      </mesh>
      <mesh position={[-0.2, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0, 0.03, 0.4, 8]} />
        <meshBasicMaterial 
          color="#ff4400"
          transparent 
          opacity={0.4}
        />
      </mesh>
    </group>
  )
}

function GlobeObject({ setActivePoint, activePoint, highlightedMutant, setHighlightedMutant }: { 
  setActivePoint: (index: number | null) => void, 
  activePoint: number | null,
  highlightedMutant: string | null,
  setHighlightedMutant: (name: string | null) => void 
}) {
  const earthRef = useRef<THREE.Mesh>(null)
  const atmosphereRef = useRef<THREE.Mesh>(null)
  const glowRef = useRef<THREE.Mesh>(null)
  const pointRefs = useRef<(THREE.Mesh | null)[]>([])
  const [hoveredPoint, setHoveredPoint] = useState<number | null>(null)

  const earthTexture = useLoader(THREE.TextureLoader, '/earth.jpg')
  const iconTextures = points.map(point => useLoader(THREE.TextureLoader, point.iconUrl))

  useFrame((state) => {
    if (glowRef.current) {
      glowRef.current.rotation.y += 0.001
    }
    pointRefs.current.forEach((mesh, index) => {
      if (mesh && points[index].name.includes(highlightedMutant || '')) {
        mesh.scale.setScalar(1.5)
      } else if (mesh) {
        mesh.scale.setScalar(1)
      }
    })
  })

  useEffect(() => {
    return () => {
    };
  }, []);

  return (
    <group>
      {/* Une seule comète suffit puisqu'elles sont rares */}
      <Comet />

      {/* Objets spatiaux */}
      <SpaceObject 
        position={[2, 1, -1]} 
        icon="/icons/radiation.png" 
        color="#ff0000" 
        scale={0.8}
      />
      <SpaceObject 
        position={[-2, -1, 1]} 
        icon="/icons/biohazard.png" 
        color="#00ff00" 
        scale={0.8}
      />
      <SpaceObject 
        position={[0, 2, 0]} 
        icon="/icons/warning.png" 
        color="#ffff00" 
        scale={0.8}
      />

      {/* Satellites avec différentes images */}
      <Satellite radius={1.4} speed={0.3} offset={0} image="/satellites/roche.png" color="#d4d4d4" />
      <Satellite radius={1.6} speed={-0.4} offset={2} image="/satellites/roche.png" color="#c0c0c0" />
      <Satellite radius={1.5} speed={0.5} offset={4} image="/satellites/sat.png" color="#b8b8b8" />
      <Satellite radius={1.7} speed={-0.3} offset={1} />
      <Satellite radius={1.3} speed={0.4} offset={3} />

      {/* Aura externe rouge */}
      <mesh ref={glowRef} scale={[1.2, 1.2, 1.2]}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshBasicMaterial
          color="#ff0000"
          transparent
          opacity={0.1}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Aura interne verte */}
      <mesh scale={[1.15, 1.15, 1.15]}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          transparent
          opacity={0.05}
          color="#00ff00"
          side={THREE.BackSide}
        />
      </mesh>

      {/* Globe terrestre */}
      <mesh ref={earthRef}>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial 
          map={earthTexture}
          metalness={0.1}
          roughness={0.8}
        />
      </mesh>

      {/* Atmosphère */}
      <mesh ref={atmosphereRef}>
        <sphereGeometry args={[1.05, 64, 64]} />
        <meshStandardMaterial
          transparent
          opacity={0.1}
          color="#ffffff"
          side={THREE.BackSide}
        />
      </mesh>

      {/* Points d'intérêt */}
      {points.map((point, index) => (
        <group key={index} position={point.position as [number, number, number]}>
          <Billboard
            follow={true}
            lockX={false}
            lockY={false}
            lockZ={false}
          >
            <mesh 
              ref={el => pointRefs.current[index] = el}
              onClick={() => setActivePoint(index)}
              onPointerEnter={() => setHoveredPoint(index)}
              onPointerLeave={() => setHoveredPoint(null)}
            >
              <planeGeometry args={[0.15, 0.15]} />
              <meshBasicMaterial 
                map={iconTextures[index]}
                transparent
                opacity={1}
                depthWrite={false}
                color={point.color}
              />
          </mesh>
          </Billboard>
        </group>
      ))}
    </group>
  )
}

// Créer un composant Globe sans SSR
const GlobeWithNoSSR = dynamic(() => Promise.resolve(Globe), {
  ssr: false
})

// Exporter le composant sans SSR par défaut
export default function GlobeWrapper() {
  return <GlobeWithNoSSR />
}

// Le composant Globe original devient une fonction nommée
function Globe() {
  const [activePoint, setActivePoint] = useState<number | null>(null)
  const [highlightedMutant, setHighlightedMutant] = useState<string | null>(null)
  const [showSolutions, setShowSolutions] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleStartGame = async () => {
    try {
        await startGame();
        // Commencer à surveiller l'état du jeu
        const interval = setInterval(async () => {
            const state = await getGameState();
            // Mettre à jour l'interface en fonction de l'état
        }, 1000);
        return () => clearInterval(interval);
    } catch (error) {
        console.error('Erreur lors du démarrage du jeu:', error);
    }
  }

  useEffect(() => {
    return () => {
    };
  }, []);

  return (
    <div className="relative w-full h-full">
      <BackgroundMusic />
      {/* Panneau latéral gauche */}
      <div className="fixed left-8 top-1/2 -translate-y-1/2 bg-black/90 rounded-2xl shadow-xl p-8 w-[350px] border border-gray-800 z-20">
        <div className="relative mb-6">
          <h2 className="text-3xl font-black text-white uppercase tracking-wider mb-4 flex items-center gap-3">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 to-red-600">
              ESPÈCES RADIOACTIVES
            </span>
            <span className="text-2xl">☢️</span>
            <div className="h-1 w-24 bg-gradient-to-r from-yellow-400 to-red-600 rounded-full mt-2"></div>
          </h2>
        </div>

        <div className="space-y-6">
          {/* Liste des animaux mutants */}
          <div className="space-y-4">
            {[
              {
                name: "Gorille Dimensionnel",
                power: "Altération de la réalité",
                description: "Capable de manipuler le tissu même de la réalité, créant des distorsions spatio-temporelles à volonté.",
                dangerLevel: "Niveau 5",
                pointIndex: 0,
                color: "red"
              },
              {
                name: "Cheval Philosophe",
                power: "Intelligence Supérieure",
                description: "Un QI de 40 fois supérieur à la moyenne humaine, capable de résoudre des équations quantiques tout en galopant.",
                dangerLevel: "Niveau 4",
                pointIndex: 1,
                color: "green"
              },
              {
                name: "Baleine Psychique",
                power: "Manipulation Émotionnelle",
                description: "Ses ondes cérébrales modifiées peuvent influencer les émotions et la sensibilité des êtres vivants à des kilomètres.",
                dangerLevel: "Niveau 3",
                pointIndex: 2,
                color: "blue"
              }
            ].map((mutant, index) => (
              <div 
                key={index}
                className="relative bg-gray-900/50 rounded-lg p-4 border border-gray-800 hover:border-yellow-500 transition-colors group cursor-pointer"
                onClick={() => {
                  setActivePoint(mutant.pointIndex)
                  setHighlightedMutant(mutant.name)
                }}
                onMouseEnter={() => setHighlightedMutant(mutant.name)}
                onMouseLeave={() => setHighlightedMutant(null)}
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    {mutant.name}
                    <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">
                      {mutant.dangerLevel}
                    </span>
                  </h3>
                </div>
                <div className="space-y-2">
                  <p className="text-sm">
                    <span className="text-yellow-400 font-bold">Capacité:</span>
                    <span className="text-yellow-100"> {mutant.power}</span>
                  </p>
                  <p className="text-sm text-gray-400 italic">
                    {mutant.description}
                  </p>
                </div>
                <div className="absolute left-0 top-0 w-1 h-full bg-yellow-500/30 rounded-l-lg group-hover:bg-yellow-500/60 transition-colors"></div>
              </div>
            ))}
          </div>

          {/* Footer */}
          <div className="mt-6 pt-4 border-t border-gray-800">
            <p className="text-xs text-yellow-500/60 text-center font-mono">
              ⚠️ DONNÉES CLASSIFIÉES - 2040 ⚠️
            </p>
          </div>
        </div>
      </div>

      {/* Titre du frfrsite */}
      <div className="absolute top-8 left-1/2 -translate-x-1/2 z-10 text-center">
        <h1 className="text-6xl font-black text-white uppercase tracking-widest mb-2 relative">
          MUTATION JEU
          <div className="absolute -bottom-2 left-0 w-full h-1 bg-gradient-to-r from-green-400 via-red-400 to-blue-400 rounded-full"></div>
        </h1>
      </div>

      {/* Bouton d'information urgent */}
      <div className="fixed top-8 right-8 z-20">
        <button 
          className="relative group bg-red-900/60 hover:bg-red-800/80 p-4 rounded-xl border-2 border-red-500/50 hover:border-red-400 transition-all duration-300 shadow-lg hover:shadow-red-500/20"
          onClick={() => setShowSolutions(true)}
        >
          <div className="absolute -top-1 -right-1 w-3 h-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-2xl">⚠️</span>
            <span className="text-red-100 font-bold uppercase tracking-wider">Solutions d'Urgence</span>
          </div>
          <div className="absolute -bottom-2 left-0 w-full h-1 bg-red-400/50 rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
        </button>
      </div>

    <div className="w-full h-full">
        <Canvas 
          camera={{ 
            position: [0, 0, 3.2], 
            fov: 45
          }}
        >
          
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
          <GlobeObject 
            setActivePoint={setActivePoint} 
            activePoint={activePoint}
            highlightedMutant={highlightedMutant}
            setHighlightedMutant={setHighlightedMutant}
          />
          <OrbitControls 
            enableZoom={false}
            minPolarAngle={Math.PI / 2.2}
            maxPolarAngle={Math.PI / 1.8}
          />
      </Canvas>
      </div>

      {/* Bulle d'information */}
      <div 
        className={`fixed right-8 top-1/2 -translate-y-1/2 bg-black/90 rounded-2xl shadow-xl p-8 w-[450px] transform transition-all duration-300 ${
          activePoint !== null ? 'translate-x-0 opacity-100' : 'translate-x-[200%] opacity-0'
        }`}
      >
        {activePoint !== null && (
          <>
            <button 
              onClick={() => setActivePoint(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-200"
            >
              ✕
            </button>
            <div className="relative mb-6">
              <h2 className={`text-5xl font-black tracking-tight mb-2 uppercase relative z-10 ${
                points[activePoint].color === 'green' ? 'text-green-400' :
                points[activePoint].color === 'red' ? 'text-red-400' :
                'text-blue-400'
              }`}>
                <span className="relative">
                  {points[activePoint].name}
                  <span className={`absolute -bottom-2 left-0 w-full h-1 transform scale-x-0 transition-transform duration-300 origin-left ${
                    points[activePoint].color === 'green' ? 'bg-green-500' :
                    points[activePoint].color === 'red' ? 'bg-red-500' :
                    'bg-blue-500'
                  } group-hover:scale-x-100`}></span>
                </span>
              </h2>
              <div className={`absolute -left-4 top-0 w-1 h-full transform origin-top transition-transform duration-500 ${
                points[activePoint].color === 'green' ? 'bg-green-500' :
                points[activePoint].color === 'red' ? 'bg-red-500' :
                'bg-blue-500'
              }`}></div>
              <div className={`absolute -top-2 -left-6 text-xs font-mono opacity-50 ${
                points[activePoint].color === 'green' ? 'text-green-400' :
                points[activePoint].color === 'red' ? 'text-red-400' :
                'text-blue-400'
              }`}>
                2040
              </div>
            </div>

            {/* Image de la créature */}
            <div className="relative w-full h-48 mb-6 rounded-lg overflow-hidden">
              <img
                src={points[activePoint].imageUrl}
                alt={`Créature mutante de ${points[activePoint].name}`}
                className="object-cover w-full h-full"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
            </div>

            <div className="space-y-6">
              <div>
                <h3 className={`text-lg font-semibold mb-2 ${
                  points[activePoint].color === 'green' ? 'text-green-300' :
                  points[activePoint].color === 'red' ? 'text-red-300' :
                  'text-blue-300'
                }`}>
                  Situation en 2040
                </h3>
                <p className="text-gray-300 leading-relaxed">
                  {points[activePoint].description}
                </p>
              </div>
              <div>
                <h3 className={`text-lg font-semibold mb-2 ${
                  points[activePoint].color === 'green' ? 'text-green-300' :
                  points[activePoint].color === 'red' ? 'text-red-300' :
                  'text-blue-300'
                }`}>
                  Créatures Mutantes
                </h3>
                <p className="text-gray-300 leading-relaxed italic">
                  {points[activePoint].crazyStory}
                </p>
              </div>
            </div>

            {/* Bouton Play - Maintenant "VA SAUVER LE MONDE" */}
            <button 
              className={`mt-8 w-full font-bold py-4 px-6 rounded-lg flex items-center justify-center space-x-3 transition-all transform hover:scale-105 ${
                points[activePoint].color === 'green' ? 'bg-gradient-to-r from-green-500 to-green-600' :
                points[activePoint].color === 'red' ? 'bg-gradient-to-r from-red-500 to-red-600' :
                'bg-gradient-to-r from-blue-500 to-blue-600'
              } text-white uppercase tracking-wider shadow-lg hover:shadow-xl relative overflow-hidden`}
              onClick={async () => {
                try {
                  setIsLoading(true);
                  let gameType = activePoint === 0 ? "gorilla" : 
                                 activePoint === 1 ? "horse" : 
                                 "whale";
                  const result = await startGame(gameType);
                  if (result.status === "started") {
                    console.log(`Mini-jeu ${gameType} lancé !`);
                    playSound('splash');
                  }
                } catch (error) {
                  console.error("Erreur détaillée:", error);
                  alert("Erreur de connexion au serveur. Vérifiez que le backend est lancé.");
                } finally {
                  setIsLoading(false);
                }
              }}
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                    <div className="w-full h-1 bg-white/20 rounded-full overflow-hidden">
                      <div className="h-full bg-white/80 rounded-full animate-progress"></div>
                    </div>
                  </div>
                  <span className="opacity-50">CHARGEMENT...</span>
                </>
              ) : (
                <span className="font-black">{points[activePoint].buttonText}</span>
              )}
            </button>
          </>
        )}
      </div>

      {/* Modale des solutions */}
      {showSolutions && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-gray-900/90 rounded-2xl p-8 max-w-2xl w-full mx-4 border border-red-500/30">
            <div className="flex justify-between items-start mb-6">
              <h2 className="text-3xl font-black text-red-400">SOLUTIONS D'URGENCE - 2040</h2>
              <button 
                onClick={() => setShowSolutions(false)}
                className="text-gray-400 hover:text-gray-200"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-6 text-gray-300">
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-red-300">Actions Immédiates Requises :</h3>
                <ul className="list-disc ml-6 space-y-3">
                  <li>Mise en place immédiate de filtres de décontamination dans les zones touchées</li>
                  <li>Développement de technologies de neutralisation des radiations</li>
                  <li>Création de sanctuaires protégés pour les espèces non-mutées</li>
                  <li>Programme de recherche sur la réversion des mutations</li>
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-bold text-yellow-300">Prévention pour le Passé :</h3>
                <ul className="list-disc ml-6 space-y-3">
                  <li>Transition immédiate vers les énergies renouvelables</li>
                  <li>Renforcement des normes de sécurité nucléaire</li>
                  <li>Protection accrue des écosystèmes naturels</li>
                  <li>Éducation mondiale sur les risques de la pollution radioactive</li>
                </ul>
              </div>

              <div className="mt-8 p-4 bg-red-900/20 rounded-lg border border-red-500/30">
                <p className="text-red-300 font-mono text-sm">
                  ⚠️ AVERTISSEMENT : Ces informations sont transmises depuis 2040 pour prévenir cette timeline. Agissez maintenant.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}