import { TrendingUp, Calendar, BarChart3, Eye, EyeOff } from "lucide-react";
import { useState } from "react";

export default function FinancialTrends({ data }) {
  const [activeTab, setActiveTab] = useState("monthly");
  const [showCategories, setShowCategories] = useState(false);

  const getTrendData = () => {
    switch (activeTab) {
      case "monthly":
        return data.monthly_financial_trends;
      case "quarterly":
        return data.quarterly_trends;
      case "yearly":
        return data.yearly_trends;
      case "weekly":
        return data.day_of_week_patterns;
      default:
        return data.monthly_financial_trends;
    }
  };

  const getGrowthData = () => {
    if (activeTab === "monthly") return data.month_over_month_growth;
    if (activeTab === "yearly") return data.year_over_year_growth;
    return null;
  };

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-violet-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-violet-500/20 bg-violet-500/10">
            <TrendingUp className="h-6 w-6 text-violet-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              Financial Trends
            </h3>
            <p className="text-sm text-gray-400">
              Time-based financial performance analysis
            </p>
          </div>
        </div>
        {data.category_trends_over_time && (
          <button
            onClick={() => setShowCategories(!showCategories)}
            className="flex items-center gap-2 rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-2 text-sm font-medium text-violet-400 transition-colors hover:bg-violet-500/20"
          >
            {showCategories ? (
              <>
                <EyeOff className="h-4 w-4" /> Hide Categories
              </>
            ) : (
              <>
                <Eye className="h-4 w-4" /> Show Categories
              </>
            )}
          </button>
        )}
      </div>

      <hr className="my-2 border-gray-700" />

      {/* Time Period Tabs */}
      <div className="flex gap-2 mb-4">
        {data.monthly_financial_trends && (
          <button
            onClick={() => setActiveTab("monthly")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === "monthly"
                ? "bg-violet-600 text-white"
                : "bg-white/5 text-gray-400 hover:bg-white/10"
            }`}
          >
            Monthly
          </button>
        )}
        {data.quarterly_trends && (
          <button
            onClick={() => setActiveTab("quarterly")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === "quarterly"
                ? "bg-violet-600 text-white"
                : "bg-white/5 text-gray-400 hover:bg-white/10"
            }`}
          >
            Quarterly
          </button>
        )}
        {data.yearly_trends && (
          <button
            onClick={() => setActiveTab("yearly")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === "yearly"
                ? "bg-violet-600 text-white"
                : "bg-white/5 text-gray-400 hover:bg-white/10"
            }`}
          >
            Yearly
          </button>
        )}
        {data.day_of_week_patterns && (
          <button
            onClick={() => setActiveTab("weekly")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === "weekly"
                ? "bg-violet-600 text-white"
                : "bg-white/5 text-gray-400 hover:bg-white/10"
            }`}
          >
            Day of Week
          </button>
        )}
      </div>

      {/* Daily Trends Summary */}
      {data.daily_trends_summary && (
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="rounded-lg bg-white/5 p-4">
            <p className="text-sm text-gray-400">Avg Daily Amount</p>
            <p className="text-lg font-bold text-violet-400">
              $
              {data.daily_trends_summary.average_daily_amount?.toLocaleString()}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4">
            <p className="text-sm text-gray-400">Avg Daily Transactions</p>
            <p className="text-lg font-bold text-violet-400">
              {data.daily_trends_summary.average_daily_transactions?.toLocaleString()}
            </p>
          </div>
        </div>
      )}

      {/* Trend Data */}
      <div className="space-y-4">
        <h4 className="text-lg font-semibold text-gray-300 capitalize">
          {activeTab === "weekly" ? "Day of Week" : activeTab} Trends
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {getTrendData()
            ?.slice(-12)
            .map((item) => {
              const period =
                item.month || item.quarter || item.year || item.day_of_week;
              const amount = item.total_amount;
              const count = item.transaction_count;

              return (
                <div
                  key={period}
                  className="flex items-center justify-between rounded-lg bg-white/5 p-3 hover:bg-white/10 transition-colors"
                >
                  <div>
                    <p className="text-sm font-medium text-white">{period}</p>
                    <p className="text-xs text-gray-400">
                      {count} transactions
                    </p>
                  </div>
                  <p className="font-bold text-violet-400">
                    ${amount?.toLocaleString()}
                  </p>
                </div>
              );
            })}
        </div>
      </div>

      {/* Growth Data */}
      {getGrowthData() && (
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-gray-300">
            {activeTab === "monthly" ? "Month-over-Month" : "Year-over-Year"}{" "}
            Growth
          </h4>
          <div className="space-y-2">
            {getGrowthData()
              ?.slice(-6)
              .map((growth) => {
                const period = growth.month || growth.year;
                const isPositive = growth.growth_rate_percent >= 0;

                return (
                  <div
                    key={period}
                    className="flex items-center justify-between rounded-lg bg-white/5 p-3"
                  >
                    <span className="text-sm text-gray-300">{period}</span>
                    <div className="flex items-center gap-2">
                      <span
                        className={`font-semibold ${
                          isPositive ? "text-green-400" : "text-red-400"
                        }`}
                      >
                        {isPositive ? "+" : ""}
                        {growth.growth_rate_percent?.toFixed(1)}%
                      </span>
                      {growth.absolute_change && (
                        <span className="text-xs text-gray-500">
                          (${Math.abs(growth.absolute_change)?.toLocaleString()}
                          )
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      )}

      {/* Category Trends */}
      {showCategories && data.category_trends_over_time && (
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-gray-300">
            Category Trends Over Time
          </h4>
          <div className="space-y-4">
            {data.category_trends_over_time.slice(0, 5).map((categoryData) => (
              <div
                key={categoryData.category}
                className="rounded-xl bg-white/5 p-4"
              >
                <h5 className="font-semibold text-white mb-3">
                  {categoryData.category}
                </h5>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                  {categoryData.monthly_data.slice(-8).map((monthData) => (
                    <div
                      key={monthData.month}
                      className="flex flex-col items-center rounded-lg bg-white/5 p-2"
                    >
                      <span className="text-xs text-gray-400">
                        {monthData.month}
                      </span>
                      <span className="text-sm font-bold text-violet-400">
                        ${monthData.amount?.toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
