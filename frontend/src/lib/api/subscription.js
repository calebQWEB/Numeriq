export async function getSubscription(session) {
  try {
    if (!session) {
      throw new Error("User not authenticated");
    }

    const response = await fetch("/api/subscription", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to fetch subscription");
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}
