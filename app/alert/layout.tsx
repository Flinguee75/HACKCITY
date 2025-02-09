import "../globals.css"
import "./styles.css"
import { Inter } from "next/font/google"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "Space System Visualization",
  description: "Explore the wonders of our cosmic neighborhood",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-space-dark text-white`}>
        {children}
      </body>
    </html>
  )
}

