import {
  CreditCard,
  Eye,
  EyeOff,
  TrendingUp,
  TrendingDown,
} from "lucide-react";
import { useState } from "react";

export default function AccountPerformance({ data }) {
  const [showAll, setShowAll] = useState(false);
  const [activeTab, setActiveTab] = useState("volume");

  const displayAccounts = showAll
    ? data.account_performance
    : data.account_performance?.slice(0, 5);

  const getTabData = () => {
    switch (activeTab) {
      case "volume":
        return (
          data.top_accounts?.highest_volume ||
          data.account_performance?.slice(0, 10)
        );
      case "active":
        return data.top_accounts?.most_active || [];
      case "volatile":
        return data.top_accounts?.most_volatile || [];
      default:
        return displayAccounts;
    }
  };

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-indigo-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-indigo-500/20 bg-indigo-500/10">
            <CreditCard className="h-6 w-6 text-indigo-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              Account Performance
            </h3>
            <p className="text-sm text-gray-400">
              Financial performance by account
            </p>
          </div>
        </div>
        {data.account_performance?.length > 5 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="flex items-center gap-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-4 py-2 text-sm font-medium text-indigo-400 transition-colors hover:bg-indigo-500/20"
          >
            {showAll ? (
              <>
                <EyeOff className="h-4 w-4" /> Show Less
              </>
            ) : (
              <>
                <Eye className="h-4 w-4" /> Show All
              </>
            )}
          </button>
        )}
      </div>

      <hr className="my-2 border-gray-700" />

      {data.top_accounts && (
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setActiveTab("volume")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === "volume"
                ? "bg-indigo-600 text-white"
                : "bg-white/5 text-gray-400 hover:bg-white/10"
            }`}
          >
            Highest Volume
          </button>
          <button
            onClick={() => setActiveTab("active")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === "active"
                ? "bg-indigo-600 text-white"
                : "bg-white/5 text-gray-400 hover:bg-white/10"
            }`}
          >
            Most Active
          </button>
          <button
            onClick={() => setActiveTab("volatile")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === "volatile"
                ? "bg-indigo-600 text-white"
                : "bg-white/5 text-gray-400 hover:bg-white/10"
            }`}
          >
            Most Volatile
          </button>
        </div>
      )}

      <div className="space-y-4">
        {getTabData()?.map((account, index) => (
          <div
            key={account.account}
            className="flex items-center justify-between rounded-xl bg-white/5 p-4 transition-colors duration-200 hover:bg-white/10"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-sm font-bold text-white shadow-md">
                {index + 1}
              </div>
              <div>
                <h4 className="font-semibold text-white truncate max-w-[200px]">
                  {account.account}
                </h4>
                <p className="text-sm text-gray-400">
                  {account.percentage_of_total?.toFixed(1)}% of total
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-bold text-indigo-400">
                ${account.total_amount?.toLocaleString()}
              </p>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <span>{account.transaction_count} transactions</span>
                {account.monthly_activity_trend && (
                  <div className="flex items-center gap-1">
                    {account.monthly_activity_trend === "increasing" ? (
                      <TrendingUp className="h-3 w-3 text-green-400" />
                    ) : (
                      <TrendingDown className="h-3 w-3 text-red-400" />
                    )}
                    <span className="text-xs">
                      {account.monthly_activity_trend}
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {displayAccounts?.length > 0 && (
        <div className="grid grid-cols-3 gap-4 mt-4">
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Avg Transaction</p>
            <p className="text-lg font-bold text-indigo-400">
              $
              {(
                displayAccounts.reduce(
                  (sum, acc) => sum + acc.average_transaction,
                  0
                ) / displayAccounts.length
              )?.toLocaleString()}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Most Volatile</p>
            <p className="text-lg font-bold text-red-400">
              $
              {Math.max(
                ...displayAccounts.map((acc) => acc.amount_volatility)
              )?.toLocaleString()}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Total Accounts</p>
            <p className="text-lg font-bold text-indigo-400">
              {data.account_performance?.length}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
