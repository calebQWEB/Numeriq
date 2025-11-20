"use client";
import { getSubscription } from "@/lib/api/subscription";
import { useAuth } from "@/provider/AuthProvider";
import { LogIn, LogOut, TrendingUp, UserPlus } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import CreditUsage from "./CreditUsage";

export default function Navbar() {
  const { user, session, loading, signOut } = useAuth();
  const [subscription, setSubscription] = useState(null);
  const [subscriptionError, setSubscriptionError] = useState(null);
  const [subscriptionLoading, setSubscriptionLoading] = useState(false);

  const router = useRouter();

  const handleSignOut = async () => {
    try {
      await signOut();
      router.push("/login");
      console.log("User signed out successfully");
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  const subscriptionStatus = async () => {
    setSubscriptionLoading(true);
    setSubscriptionError(null);

    try {
      const data = await getSubscription(session);
      setSubscription(data);
      console.log("Subscription data:", data);
    } catch (error) {
      setSubscriptionError(error.message);
    } finally {
      setSubscriptionLoading(false);
    }
  };

  useEffect(() => {
    if (session) {
      subscriptionStatus();
    }
  }, [session]);

  return (
    <nav className="flex items-center justify-between px-6 py-4 lg:px-12 bg-gray-900 text-gray-200 shadow-md">
      {/* Logo/Brand */}
      <Link
        href="/"
        className="flex items-center space-x-2 transition-transform duration-300 hover:scale-105"
      >
        <TrendingUp size={30} className="text-blue-400" />
        <span className="text-xl font-bold tracking-tight text-white">
          NumeriQ
        </span>
      </Link>

      {/* Nav Links and Auth Buttons */}
      <div className="flex items-center space-x-6">
        <Link
          href="/"
          className="text-sm font-medium transition-colors hover:text-blue-400"
        >
          Features
        </Link>
        <Link
          href="/"
          className="text-sm font-medium transition-colors hover:text-blue-400"
        >
          Pricing
        </Link>

        {loading ? (
          <div className="text-sm text-gray-400">Loading...</div>
        ) : user ? (
          // User is logged in
          <div className="flex items-center space-x-4">
            {subscription?.plan === "free" && (
              <Link
                className="rounded-full px-3 py-1 text-xs font-semibold bg-gray-700 text-gray-300 hover:bg-gray-600 transition-colors"
                href="/subscription"
              >
                Free Plan
              </Link>
            )}

            {subscription?.plan === "plus" && (
              <div className="flex items-center gap-2">
                <Link
                  href="/subcription"
                  className="rounded-full px-3 py-1 text-xs font-semibold bg-yellow-500 text-white hover:bg-yellow-400 transition-colors"
                >
                  Plus Plan
                </Link>
                <CreditUsage
                  credits={subscription.credits_left}
                  total={subscription.total_credits}
                />
              </div>
            )}

            {subscription?.plan === "pro" && (
              <div className="flex items-center gap-2">
                <Link
                  href="/subscription"
                  className="rounded-full px-3 py-1 text-xs font-bold bg-amber-500 text-black hover:bg-amber-600 transition-colors"
                >
                  Pro Plan
                </Link>
                <CreditUsage
                  credits={subscription.credits_left}
                  total={subscription.total_credits}
                />
              </div>
            )}
            <div className="flex items-center space-x-2">
              <span className="text-sm font-normal text-gray-400">
                Welcome,
              </span>
              <span className="text-sm font-medium text-white">
                {user.user_metadata.display_name || user.email}
              </span>
            </div>
            <button
              onClick={handleSignOut}
              className="inline-flex items-center space-x-2 rounded-full border border-red-500 px-4 py-2 text-sm font-semibold text-red-500 transition-colors hover:bg-red-500 hover:text-white"
            >
              <LogOut className="h-4 w-4" />
              <span>Sign Out</span>
            </button>
          </div>
        ) : (
          // User is not logged in
          <div className="flex items-center space-x-4">
            <Link
              href="/login"
              className="inline-flex items-center space-x-2 text-sm font-medium transition-colors hover:text-blue-400"
            >
              <LogIn className="h-4 w-4" />
              <span>Login</span>
            </Link>
            <Link
              href="/signup"
              className="inline-flex items-center space-x-2 rounded-full bg-blue-500 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-blue-600"
            >
              <UserPlus className="h-4 w-4" />
              <span>Sign up</span>
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
