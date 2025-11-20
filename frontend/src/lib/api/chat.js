export const getChatHistory = async (fileId, session) => {
  try {
    if (!fileId || !session) {
      throw new Error("File ID or session is missing.");
    }

    const response = await fetch(`/api/chat_history/${fileId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data; // return raw history, leave formatting for the component
  } catch (err) {
    throw new Error(`Failed to fetch chat history: ${err.message}`);
  }
};
