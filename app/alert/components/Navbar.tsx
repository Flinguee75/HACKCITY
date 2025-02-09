"use client"

import Link from "next/link"
import { motion } from "framer-motion"

const Navbar = () => {
  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 flex justify-between items-center p-4 bg-space-dark bg-opacity-70 backdrop-blur-md"
    >
      <Link href="/" className="text-2xl font-bold text-glow-blue">
        Space Explorer
      </Link>
      <ul className="flex space-x-4">
        <li>
          <Link href="/" className="hover:text-glow-blue transition-colors">
            Home
          </Link>
        </li>
        <li>
          <Link href="/explore" className="hover:text-glow-blue transition-colors">
            Explore All
          </Link>
        </li>
        <li>
          <Link href="/about" className="hover:text-glow-blue transition-colors">
            About
          </Link>
        </li>
      </ul>
    </motion.nav>
  )
}

export default Navbar

