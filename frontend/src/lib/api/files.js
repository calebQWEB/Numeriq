export const getAllFiles = async (session) => {
  try {
    if (!session) throw new Error("Not authenticated");

    const response = await fetch("/api/files", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (err) {
    throw new Error(`Failed to fetch files: ${err.message}`);
  }
};

// Fetch a single file by its ID
export const fetchFileById = async (fileId, session) => {
  if (!fileId || !session) {
    console.log("File ID or session is missing.");
    return;
  }
  try {
    const response = await fetch(`/api/files/${fileId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch file data");
    }

    return await response.json();
  } catch (error) {
    console.log("Error fetching file data:", error);
  }
};

// Upload a file
export const uploadFile = async (fileDetails, session) => {
  const file = fileDetails.file[0];
  console.log("file:", file);

  try {
    if (!session) {
      throw new Error("Not authenticated");
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("spreadsheet_type", fileDetails.spreadsheet);

    // DEBUG: Log FormData contents
    console.log("FormData entries:");
    for (let [key, value] of formData.entries()) {
      console.log(`${key}:`, value);
    }

    const response = await fetch("/api/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.log("Error response:", errorData);
      throw new Error("Upload failed");
    }
  } catch (error) {
    console.error("Upload error:", error);
  }
};

// Delete a file by Id
export const deleteFile = async (session, id) => {
  if (!session.access_token) {
    throw new Error("User is not authenticated");
  }
  if (!id) {
    throw new Error("File ID is missing");
  }
  try {
    const response = await fetch(`/api/files/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to delete file");
    }
  } catch (error) {
    console.error("Error deleting file:", error);
  }
};

// Analyze File
export const AnalyzeFile = async ({
  session,
  id,
  spreadsheet_type,
  retries = 1,
}) => {
  if (!session?.access_token) {
    throw new Error("User is not authenticated");
  }
  if (!id) {
    throw new Error("File ID is missing");
  }

  try {
    const response = await fetch(`/api/analyze/${id}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ spreadsheet_type }),
    });

    const result = await response.json();

    if (!response.ok) {
      const detail = result.detail || "Full analysis failed";

      if (detail.includes("InvalidJWT") && retries > 0) {
        toast.info("Retrying analysis due to expired token...");
        return await AnalyzeFile({
          session,
          id,
          spreadsheet_type,
          retries: retries - 1,
        });
      }

      if (detail.includes("File not found")) {
        throw new Error(
          "The uploaded file could not be found. Please re-upload and try again."
        );
      }

      throw new Error(detail);
    }

    return result; // in case caller needs it
  } catch (error) {
    console.error("File analysis error:", error);
    throw error; // important: rethrow so caller can handle it
  }
};

// Analyze with AI
export const analyzeWithAI = async (session, fileId, spreadsheet_type) => {
  try {
    const response = await fetch(`/api/ai-analyze/${fileId}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ spreadsheet_type: spreadsheet_type }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Full analysis failed");
    }
  } catch (error) {
    console.error("File analysis error:", error);
  }
};
