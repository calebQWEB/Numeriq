export const exportPdfApi = async (fileId, session) => {
  if (!fileId || !session) {
    throw new Error("File ID or session is missing.");
  }

  const response = await fetch(`/api/export/${fileId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to export PDF: ${errorText}`);
  }

  const blob = await response.blob();

  // Try to parse filename from response headers
  let filename = `${fileId}_Analysis_Report.pdf`;
  const contentDisposition = response.headers.get("content-disposition");
  if (contentDisposition) {
    const filenameMatch = contentDisposition.match(
      /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
    );
    if (filenameMatch) {
      filename = filenameMatch[1].replace(/['"]/g, "");
    }
  }

  return { blob, filename };
};
