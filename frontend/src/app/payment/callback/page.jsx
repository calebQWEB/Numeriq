"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { CheckCircle, XCircle } from "lucide-react";

export default function PaymentCallback() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState("pending");

  useEffect(() => {
    const paymentStatus = searchParams.get("status");
    if (paymentStatus === "successful") {
      setStatus("success");
    } else {
      setStatus("failed");
    }

    // Redirect back to dashboard after 4s
    const timer = setTimeout(() => {
      router.push("/dashboard");
    }, 4000);

    return () => clearTimeout(timer);
  }, [searchParams, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow-lg text-center max-w-md">
        {status === "success" ? (
          <>
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-800">
              Payment Successful 🎉
            </h1>
            <p className="text-gray-600 mt-2">
              Your subscription has been activated. Redirecting to dashboard...
            </p>
          </>
        ) : status === "failed" ? (
          <>
            <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-800">
              Payment Failed ❌
            </h1>
            <p className="text-gray-600 mt-2">
              We couldn’t verify your payment. Please try again.
            </p>
          </>
        ) : (
          <p className="text-gray-600">Processing your payment...</p>
        )}
      </div>
    </div>
  );
}
