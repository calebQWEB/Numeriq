export async function POST(request) {
  try {
    const token = request.headers.get("authorization");

    if (!token) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Get FormData from the request
    const formData = await request.formData();

    // DEBUG: Log all FormData entries
    console.log("Received FormData entries:");
    for (let [key, value] of formData.entries()) {
      console.log(`${key}:`, value);
    }

    const file = formData.get("file");
    const spreadsheetType = formData.get("spreadsheet_type");

    if (!file) {
      return new Response(JSON.stringify({ error: "No file uploaded" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Check if spreadsheetType is null/undefined
    if (!spreadsheetType) {
      console.error("spreadsheet_type is missing or null");
      return new Response(
        JSON.stringify({ error: "spreadsheet_type is required" }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    // Forward the FormData to your FastAPI backend
    const backendFormData = new FormData();
    backendFormData.append("file", file);
    backendFormData.append("spreadsheet_type", spreadsheetType);

    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      headers: {
        Authorization: token,
      },
      body: backendFormData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Backend error:", errorText);
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Server route error:", error);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
