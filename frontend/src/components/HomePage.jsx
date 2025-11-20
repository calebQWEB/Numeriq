import { ArrowRight, ChartNoAxesColumnIncreasing } from "lucide-react";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6 text-white">
      {/* Container for the content */}
      <div className="flex flex-col items-center text-center space-y-12 max-w-5xl w-full">
        {/* Main Heading and Sub-paragraph */}
        <header className="space-y-4">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight text-gray-200">
            Your Intelligent{" "}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600 drop-shadow-lg">
              AI Analyst
            </span>
            .
          </h1>
          <p className="text-base sm:text-lg text-gray-400 leading-relaxed max-w-2xl mx-auto">
            Unlock **seamless AI integration** and **powerful data insights** to
            streamline your workflows and make smarter decisions.
          </p>

          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-full shadow-lg transform transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-75"
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </Link>
        </header>

        {/* Sleek AI Analyst Card */}
        <div className="relative w-full max-w-4xl">
          <div className="w-full shadow-2xl bg-white/5 backdrop-blur-sm border border-white/10 rounded-3xl transition-all duration-500 ease-in-out hover:shadow-3xl transform hover:scale-[1.01] p-6 sm:p-8">
            {/* Card Header */}
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-white/10">
              <h2 className="text-xl sm:text-2xl font-semibold text-white">
                Sales Analysis
              </h2>
              {/* Card Controls */}
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-red-500"></span>
                <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                <span className="w-3 h-3 rounded-full bg-green-500"></span>
              </div>
            </div>

            {/* Table */}
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm text-gray-300">
                <thead className="text-xs sm:text-sm font-medium text-gray-400 uppercase tracking-wider">
                  <tr>
                    <th className="px-3 py-2 sm:px-4 sm:py-3 text-left">
                      Product
                    </th>
                    <th className="px-3 py-2 sm:px-4 sm:py-3 text-left">Q1</th>
                    <th className="px-3 py-2 sm:px-4 sm:py-3 text-left">Q2</th>
                    <th className="px-3 py-2 sm:px-4 sm:py-3 text-left">Q3</th>
                    <th className="px-3 py-2 sm:px-4 sm:py-3 text-left">Q4</th>
                    <th className="px-3 py-2 sm:px-4 sm:py-3 text-left">
                      Total
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      Laptops
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $12,300
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $15,200
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $14,500
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $18,000
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3 font-semibold text-white">
                      $60,000
                    </td>
                  </tr>
                  <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      Tablets
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $8,000
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $9,500
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $10,200
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $11,000
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3 font-semibold text-white">
                      $38,700
                    </td>
                  </tr>
                  <tr className="hover:bg-white/5 transition-colors">
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      Accessories
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $5,000
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $6,000
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $7,200
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3">
                      $6,800
                    </td>
                    <td className="text-left px-3 py-2 sm:px-4 sm:py-3 font-semibold text-white">
                      $25,000
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="flex items-center justify-center space-x-6 absolute -bottom-1/6 -right-1/6 w-[450px] shadow-2xl bg-white/5 backdrop-blur-sm border border-white/10 rounded-3xl transition-all duration-500 ease-in-out hover:shadow-3xl transform hover:scale-[1.01] p-6 sm:p-8">
            <div className="w-24 h-24 rounded-full flex items-center justify-center bg-blue-800 text-white text-3xl font-bold shadow-lg">
              AI
            </div>

            <ChartNoAxesColumnIncreasing
              strokeWidth={2.5}
              size={120}
              color="green"
            />
          </div>
        </div>
      </div>
    </main>
  );
}
