export const viewAnalysis = async (fileId, session) => {
  if (!fileId || !session) {
    setGetAnalyticsError("File ID or session is missing.");
    return;
  }
  try {
    const response = await fetch(`/api/analysis/${fileId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(result.message || "Failed to get analytics");
    }

    return await response.json();
  } catch (error) {
    console.log("Error viewing analytics:", error);
  }
};
