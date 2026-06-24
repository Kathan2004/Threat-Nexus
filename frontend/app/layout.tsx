import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Threat Nexus",
  description: "Cyber threat intelligence platform",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
