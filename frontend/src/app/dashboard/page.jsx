import AllFiles from "./_components/AllFiles";
import UploadForm from "./_components/uploadForm";

const Page = () => {
  return (
    <main className="min-h-screen p-6 sm:p-12 text-white font-sans flex flex-col items-center">
      {/* Hero Section */}
      <header className="py-16 text-center w-full">
        <h1 className="text-4xl sm:text-5xl lg:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 animate-pulse-slow">
          File Management
        </h1>
        <p className="mt-4 text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto">
          Upload, organize, and access your documents.
        </p>
      </header>

      {/* Main Content Grid */}
      <div className="px-4 flex items-start space-x-5 justify-start flex-col md:flex-row">
        <div>
          <UploadForm />
        </div>
        <AllFiles />
      </div>
    </main>
  );
};

export default Page;
