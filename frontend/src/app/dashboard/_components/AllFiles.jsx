"use client";
import { useCallback, useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { useAuth } from "@/provider/AuthProvider";
import LoadingSpinner from "@/utils/LoadingSpinner";
import Link from "next/link";
import FileCard from "./FileCard";
import { getAllFiles } from "@/lib/api";

const AllFiles = () => {
  const [allFiles, setAllFiles] = useState([]);
  const [allFilesError, setAllFilesError] = useState("");
  const [allFilesLoad, setAllFilesLoad] = useState(false);
  const { user, session } = useAuth();

  const fetchAllFiles = async () => {
    setAllFilesError("");
    setAllFilesLoad(true);

    try {
      const data = await getAllFiles(session);
      setAllFiles(data.files);
    } catch (err) {
      setAllFilesError(err.message || String(err));
    } finally {
      setAllFilesLoad(false);
    }
  };

  useEffect(() => {
    if (session) {
      fetchAllFiles();
    }
  }, [session]);

  return (
    <section>
      {/* <h1 className="text-center text-3xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight text-gray-200">
        All Files
      </h1> */}

      <div className="text-start">
        {allFilesLoad ? (
          <LoadingSpinner message="Fetching your files..." />
        ) : (
          allFiles && (
            <div className="mt-9 grid grid-cols-1 sm:grid-cols-2 gap-6">
              {allFiles.map((item) => (
                <FileCard
                  key={item.id}
                  {...item}
                  refetchFiles={fetchAllFiles}
                  allFilesLoad={allFilesLoad}
                />
              ))}
            </div>
          )
        )}

        {allFiles.length === 0 && <p>Your Files will appear here</p>}
      </div>
    </section>
  );
};

export default AllFiles;
