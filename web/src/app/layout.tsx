import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Global Empathy News",
  description: "Discover perspective gaps in global news coverage",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
