"use client";
import FileUpload from "@/components/FileUpload";
import { uploadFile } from "@/lib/api";
import { useAuth } from "@/provider/AuthProvider";
import { useState } from "react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";

const UploadForm = () => {
  const [uploading, setUploading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const { session } = useAuth();

  const handleUploadFile = async (fileDetails) => {
    try {
      await uploadFile(fileDetails, session);
      toast.success("File uploaded successfully!");
    } catch (error) {
      console.error("Upload error:", error);
      toast.error(error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit(handleUploadFile)}
      className="w-full p-8 sm:p-10 bg-white/5 backdrop-blur-lg border border-white/10 rounded-3xl shadow-2xl space-y-8 animate-fade-in"
    >
      {/* Form Title */}
      <h2 className="text-3xl font-bold text-gray-100 text-center">
        Upload a New Files
      </h2>

      {/* Section for Spreadsheet Type selection. */}
      <div className="space-y-4">
        <label
          htmlFor="spreadsheet"
          className="block text-lg font-semibold text-gray-200"
        >
          Spreadsheet Type
        </label>
        <div className="relative">
          {/* Styled select dropdown to match the dark theme. */}
          <select
            id="spreadsheet"
            name="spreadsheet"
            {...register("spreadsheet", { required: "Please select a type" })}
            className="w-full px-5 py-3 bg-white/5 border border-white/10 text-gray-300 rounded-xl appearance-none focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors"
          >
            <option value="" className="text-black">
              Select a type...
            </option>
            <option value="Sales" className="text-black">
              Sales
            </option>
            <option value="Retail" className="text-black">
              Retail
            </option>
            <option value="HR" className="text-black">
              HR
            </option>
            <option value="Finance" className="text-black">
              Finance
            </option>
            <option value="Operations" className="text-black">
              Operations
            </option>
          </select>
          {errors.spreadsheet && (
            <p className="text-red-400 text-sm mt-2">
              {errors.spreadsheet.message}
            </p>
          )}
          {/* Custom arrow for the select dropdown to maintain the sleek design. */}
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-400">
            <svg
              className="w-4 h-4"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Section for File Upload. */}
      <div className="space-y-4">
        <label
          htmlFor="file-upload"
          className="block text-lg font-semibold text-gray-200"
        >
          Upload your file
        </label>
        <FileUpload register={register} uploading={uploading} error={errors} />
      </div>

      {/* Submit button. */}
      <div className="pt-4">
        <button
          type="submit"
          disabled={uploading}
          className={`w-full py-3 rounded-xl text-white font-semibold text-lg transition-all duration-300 ease-in-out bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-blue-500 focus:ring-opacity-50 ${
            uploading ? "opacity-70 cursor-not-allowed" : ""
          }`}
        >
          {uploading ? "Uploading..." : "Upload File"}
        </button>
      </div>
    </form>
  );
};

export default UploadForm;
