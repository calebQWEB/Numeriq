import { Poppins, Raleway } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { AuthProvider } from "@/provider/AuthProvider";
import ClientToaster from "@/provider/ClientToaster";

const raleway = Raleway({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
  variable: "--font-raleway",
});

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
  variable: "--font-poppins",
});

export const metadata = {
  title: "Numeriq",
  description: "AI powered spreadsheet analyzer",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${raleway.variable} ${poppins.variable} antialiased`}>
        <AuthProvider>
          <Navbar />
          <div className="px-8 py-4">{children}</div>
          <ClientToaster />
        </AuthProvider>
      </body>
    </html>
  );
}
