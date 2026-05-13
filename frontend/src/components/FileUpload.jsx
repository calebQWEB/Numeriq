export default function FileUpload({ uploading, register, error }) {
  return (
    <div className="w-full max-w-md mx-auto">
      <div>
        {uploading ? (
          <div className="flex flex-col items-center">
            <p className="text-lg font-semibold text-gray-700 mb-3">
              Uploading...
            </p>
            <div className="w-20 h-20 border-4 border-t-4 border-blue-200 border-t-blue-500 rounded-full animate-spin"></div>
          </div>
        ) : (
          <>
            {/* Visible input */}
            <input
              type="file"
              accept=".xlsx,.xls,.csv"
              {...register("file", { required: true })}
              disabled={uploading}
              className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
            />

            {error.file && (
              <p className="text-red-400 text-sm mt-1">{error.file.message}</p>
            )}
            <p className="text-sm text-gray-500 font-medium mt-2 text-center">
              Supported formats: .xlsx, .xls, .csv
            </p>
          </>
        )}
      </div>
    </div>
  );
}
