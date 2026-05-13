"use client";

import React, { useState } from "react";
import PlanCard from "./_components/PlanCard";
import { plans } from "@/utils/constant";
import { useAuth } from "@/provider/AuthProvider";
import Result_ from "postcss/lib/result";
import LoadingSpinner from "@/utils/LoadingSpinner";

export default function PricingPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const { user, session } = useAuth();

  const initializePayment = async (plan, planPrice) => {
    const { display_name, email } = user.user_metadata;
    const amount = planPrice * 1511; // Convert to NGN
    const phone_number = user.phone || "";
    const id = user.id;

    console.log("Display name", display_name);
    console.log("Email", email);
    console.log("Amount", amount);
    console.log("phone number", phone_number);
    console.log("User id", id);
    console.log("Price", plan);

    if (!amount || !display_name || !email || !plan || !id) {
      setError("Please fill in all required fields.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const paymentData = {
        tx_ref: `sub_${id}_${plan}_${Date.now()}`,
        amount,
        currency: "NGN",
        email: email.trim(),
        name: display_name.trim(),
        phone_number: phone_number.trim(),
        payment_options: "card,mobilemoney,ussd,banktransfer",
        customizations: {
          title: "Your Numeriq Payment",
          description: `Payment for ${plan.toUpperCase()} Subscription`,
        },
        meta: {
          user_id: id,
          plan: plan,
        },
      };

      console.log("Payment Data:", paymentData);

      const response = await fetch("/api/payment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(paymentData),
      });

      const result = await response.json();

      console.log("Payment Initialization Response:", result);

      if (result.success) {
        setSuccess("Payment initialized! Redirecting...");
        // Redirect to payment link
        window.location.href = result.data.link;
      } else {
        setError(result.message || "Payment initialization failed");
      }
    } catch (error) {
      console.error("Payment error:", error);
      setError(
        "Payment initialization failed. Please check your connection and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900">
        <LoadingSpinner message="Initializing payment..." />
      </div>
    );
  }

  return (
    <div className="bg-gray-900 min-h-screen py-24 sm:py-32 font-sans text-inter">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        .font-sans {
          font-family: 'Inter', sans-serif;
        }
      `}</style>
      <div className="mx-auto max-w-7xl px-6 lg:px-8 text-center">
        <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight mb-4">
          Simple, Transparent Pricing
        </h1>
        <p className="text-lg sm:text-xl text-gray-400 max-w-3xl mx-auto mb-16">
          Find the perfect plan for your business needs. Get started with our
          powerful analysis tools today.
        </p>
        <div className="flex flex-col lg:flex-row justify-center items-stretch gap-y-12 lg:gap-x-8">
          {plans.map((plan, index) => (
            <PlanCard
              key={index}
              plan={plan}
              initializePayment={initializePayment}
            />
          ))}
        </div>

        <button
          onClick={() => {
            console.log(process.env.FLUTTERWAVE_SECRET_KEY);
          }}
        >
          {" "}
          Check ENV
        </button>
      </div>
    </div>
  );
}
