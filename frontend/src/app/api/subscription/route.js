import { NextResponse } from "next/server";

export async function GET(request) {
  try {
    // Get the Authorization header (Supabase JWT)
    const authHeader = request.headers.get("authorization");
    if (!authHeader) {
      return NextResponse.json(
        { error: "Missing authorization header" },
        { status: 401 }
      );
    }

    // Forward request to FastAPI backend
    const response = await fetch("http://localhost:8000/subscription", {
      method: "GET",
      headers: {
        Authorization: authHeader,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: errorData.detail || "Failed to fetch subscription" },
        { status: response.status }
      );
    }

    const subscription = await response.json();
    return NextResponse.json(subscription);
  } catch (error) {
    console.error("Error in /api/subscription:", error.message);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
