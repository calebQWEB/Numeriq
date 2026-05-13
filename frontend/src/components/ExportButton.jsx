import { useState } from "react";
import {
  FileText,
  Download,
  Loader2,
  CheckCircle,
  XCircle,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { exportPdfApi } from "@/lib/api";
import toast from "react-hot-toast";

const ExportButton = ({ fileId, session, isActive }) => {
  const [getFileError, setGetFileError] = useState("");
  const [isExporting, setIsExporting] = useState(false);
  const [exportError, setExportError] = useState("");
  const router = useRouter();

  const exportPDF = async () => {
    if (!isActive) {
      router.push("/subscription");
      return;
    }

    setIsExporting(true);
    setExportError("");

    try {
      const { blob, filename } = await exportPdfApi(fileId, session);

      // Download logic stays in UI layer
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();

      // Clean up
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);

      toast.success("PDF report downloaded successfully!"); // or toast
    } catch (error) {
      toast.error("Failed to Export PDF");
      setExportError(error.message || "An error occurred while exporting PDF");
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="relative">
      {/* Export Button */}
      <button
        onClick={exportPDF}
        disabled={isExporting}
        className={`
          group relative inline-flex items-center gap-2 px-6 py-3 
          bg-gradient-to-r from-blue-600 to-blue-700 
          hover:from-blue-700 hover:to-blue-800
          text-white font-semibold rounded-lg
          shadow-lg hover:shadow-xl
          transform transition-all duration-200
          hover:scale-105 active:scale-95
          disabled:opacity-50 disabled:cursor-not-allowed
          disabled:hover:scale-100
          overflow-hidden
        `}
      >
        {/* Animated background on hover */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-blue-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>

        {/* Icon */}
        {/* <div className="relative z-10">
          {isExporting ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : exportStatus === "success" ? (
            <CheckCircle className="w-5 h-5" />
          ) : exportStatus === "error" ? (
            <XCircle className="w-5 h-5" />
          ) : (
            <FileText className="w-5 h-5" />
          )}
        </div> */}

        {/* Text */}
        <span className="relative z-10">
          {isExporting ? "Generating PDF..." : "Export to PDF"}
        </span>

        {/* Download icon */}
        {!isExporting && (
          <Download className="w-4 h-4 relative z-10 group-hover:translate-y-0.5 transition-transform" />
        )}
      </button>
    </div>
  );
};

export default ExportButton;
