"use client";
import { AnalyzeFile, deleteFile } from "@/lib/api";
import { useAuth } from "@/provider/AuthProvider";
import { ChevronDown, Trash } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

export default function FileCard({
  id,
  filename,
  spreadsheet_type,
  upload_date,
  status,
  refetchFiles,
}) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [showCard, setShowCard] = useState(false);
  const [isCardMounted, setIsCardMounted] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { session } = useAuth();
  const transitionDuration = 300; // Match this with the Tailwind duration-300 class

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      await AnalyzeFile({ session, id, spreadsheet_type });
      toast.success("Analysis successful!");
    } catch (error) {
      toast.error(error.message || "Analysis failed. Please try again.");
    } finally {
      await refetchFiles();
      setIsAnalyzing(false);
    }
  };

  const handleDeletFile = async () => {
    setIsDeleting(true);
    try {
      await deleteFile(session, id);
      toast.success("File deleted successfully");
    } catch (error) {
      console.error("Error deleting file:", error);
      toast.error(error.message || "Failed to delete file");
    } finally {
      refetchFiles();
      setIsDeleting(false);
    }
  };

  useEffect(() => {
    if (showCard) {
      // Mount the card and trigger the fade-in
      setIsCardMounted(true);
    } else {
      // Unmount the card after the fade-out transition
      const timeoutId = setTimeout(
        () => setIsCardMounted(false),
        transitionDuration
      );
      return () => clearTimeout(timeoutId);
    }
  }, [showCard]);

  return (
    <div className="flex flex-col items-center text-gray-200">
      <div className="w-full max-w-sm">
        <button
          onClick={() => setShowCard((prev) => !prev)}
          className="mb-3 min-w-sm cursor-pointer flex items-center justify-between px-4 w-full h-14 bg-white/5 backdrop-blur-lg border border-white/10 rounded-xl shadow-2xl transition-transform duration-300 ease-in-out transform"
        >
          <span className="text-sm font-medium truncate max-w-[calc(100%-80px)]">
            {filename}
          </span>
          <ChevronDown
            color="gray"
            className={showCard ? "transform rotate-180" : ""}
          />
        </button>

        <div
          className={`
            relative w-full overflow-hidden transition-all duration-300 ease-in-out
            ${isCardMounted ? "max-h-96 opacity-100" : "max-h-0 opacity-0"}
          `}
        >
          <div
            className={`
              p-6 w-full max-w-sm bg-white/5 backdrop-blur-xl rounded-2xl shadow-xl border border-white/10 cursor-pointer
              transition-opacity duration-300 ease-in-out
            `}
          >
            <div className="absolute inset-0 rounded-2xl pointer-events-none border border-transparent group-hover:border-blue-500 transition-colors duration-300"></div>

            <div className="flex items-center justify-between mb-7">
              <p className="text-sm text-gray-300 font-medium">
                Uploaded:{" "}
                {new Date(upload_date).toLocaleString("en-US", {
                  dateStyle: "medium",
                  timeStyle: "short",
                })}
              </p>
              <button onClick={handleDeletFile}>
                {isDeleting ? (
                  <span className="animate-pulse">
                    <Trash className="w-5 h-5 text-red-500" />
                  </span>
                ) : (
                  <Trash className="w-5 h-5 text-gray-400 hover:text-red-500 transition-colors duration-300" />
                )}
              </button>
            </div>

            <div className="flex items-center justify-between mb-4">
              <h3 className="text-2xl font-semibold text-white truncate max-w-[calc(100%-80px)]">
                {filename}
              </h3>
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide
                  ${
                    status === "analyzed"
                      ? "bg-green-600/20 text-green-300 border border-green-500/30"
                      : status === "processing"
                      ? "bg-yellow-600/20 text-yellow-300 border border-yellow-500/30 animate-pulse"
                      : status === "failed" || status === "error"
                      ? "bg-red-600/20 text-red-300 border border-red-500/30"
                      : "bg-gray-600/20 text-gray-300 border border-gray-500/30"
                  }`}
              >
                {isAnalyzing ? "processing..." : status}
              </span>
            </div>

            <div className="mt-5 grid gap-3">
              {status === "uploaded" ||
              status === "error" ||
              status === "failed" ? (
                <button
                  className={`w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg shadow-md
                    hover:from-blue-700 hover:to-purple-700 transition-all duration-300 ease-in-out transform hover:scale-[1.02]
                    focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-75
                    ${isAnalyzing ? "opacity-60 cursor-not-allowed" : ""}`}
                  disabled={isAnalyzing}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleAnalyze();
                  }}
                >
                  {isAnalyzing ? "Analyzing..." : "Analyze File"}
                </button>
              ) : (
                <>
                  <Link
                    href={`/analysis/${id}`}
                    className="group w-full inline-flex items-center justify-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg shadow-md
                      hover:from-blue-700 hover:to-purple-700 transition-all duration-300 ease-in-out transform hover:scale-[1.02]
                      focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-75"
                    onClick={(e) => {
                      e.stopPropagation();
                    }}
                  >
                    View Analytics
                    <span className="ml-2 group-hover:translate-x-1 transition-transform duration-200">
                      →
                    </span>
                  </Link>
                  <Link
                    href={`/chat/${id}`}
                    className="w-full inline-flex items-center justify-center px-6 py-3 bg-white/10 text-gray-200 font-medium rounded-lg shadow-md border border-white/20
                      hover:bg-white/20 hover:text-white transition-all duration-300 ease-in-out transform hover:scale-[1.02]
                      focus:outline-none focus:ring-4 focus:ring-gray-400 focus:ring-opacity-50"
                    onClick={(e) => e.stopPropagation()}
                  >
                    Ask AI
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
