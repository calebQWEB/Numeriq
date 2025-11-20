import { Building2, Eye, EyeOff, TrendingUp, TrendingDown } from "lucide-react";
import { useState } from "react";

export default function DepartmentPerformance({ data }) {
  const [showAll, setShowAll] = useState(false);
  const [showBreakdown, setShowBreakdown] = useState(false);

  // Check if it's department or segment data
  const isDepartment = !!data.department_financials;
  const financialsData = data.department_financials || data.segment_financials;
  const breakdownData =
    data.department_category_breakdown || data.segment_category_breakdown;
  const title = isDepartment ? "Department Performance" : "Segment Performance";
  const itemLabel = isDepartment ? "department" : "segment";

  const displayItems = showAll ? financialsData : financialsData?.slice(0, 5);

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-cyan-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-cyan-500/20 bg-cyan-500/10">
            <Building2 className="h-6 w-6 text-cyan-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              {title}
            </h3>
            <p className="text-sm text-gray-400">
              Financial performance by {itemLabel}
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          {breakdownData && (
            <button
              onClick={() => setShowBreakdown(!showBreakdown)}
              className="flex items-center gap-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-400 transition-colors hover:bg-cyan-500/20"
            >
              <Eye className="h-4 w-4" />
              {showBreakdown ? "Hide" : "Show"} Breakdown
            </button>
          )}
          {financialsData?.length > 5 && (
            <button
              onClick={() => setShowAll(!showAll)}
              className="flex items-center gap-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-400 transition-colors hover:bg-cyan-500/20"
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
      </div>

      <hr className="my-2 border-gray-700" />

      <div className="space-y-4">
        {displayItems?.map((item, index) => (
          <div
            key={item[itemLabel]}
            className="flex items-center justify-between rounded-xl bg-white/5 p-4 transition-colors duration-200 hover:bg-white/10"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-cyan-600 text-sm font-bold text-white shadow-md">
                {index + 1}
              </div>
              <div>
                <h4 className="font-semibold text-white truncate max-w-[200px]">
                  {item[itemLabel]}
                </h4>
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  <span>{item.percentage_of_total?.toFixed(1)}% of total</span>
                  {item.growth_trend_percentage && (
                    <div className="flex items-center gap-1">
                      {item.growth_trend_percentage > 0 ? (
                        <TrendingUp className="h-3 w-3 text-green-400" />
                      ) : (
                        <TrendingDown className="h-3 w-3 text-red-400" />
                      )}
                      <span
                        className={`text-xs ${
                          item.growth_trend_percentage > 0
                            ? "text-green-400"
                            : "text-red-400"
                        }`}
                      >
                        {Math.abs(item.growth_trend_percentage).toFixed(1)}%
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="text-right">
              <p className="font-bold text-cyan-400">
                ${item.total_amount?.toLocaleString()}
              </p>
              <div className="text-sm text-gray-400">
                <p>{item.transaction_count} transactions</p>
                <p>Avg: ${item.average_transaction?.toLocaleString()}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {showBreakdown && breakdownData && (
        <div className="mt-6">
          <h4 className="text-lg font-semibold text-gray-300 mb-4">
            Category Breakdown by {isDepartment ? "Department" : "Segment"}
          </h4>
          <div className="space-y-4">
            {breakdownData.map((dept) => (
              <div
                key={dept.department || dept.segment}
                className="rounded-xl bg-white/5 p-4"
              >
                <h5 className="font-semibold text-white mb-3">
                  {dept.department || dept.segment}
                </h5>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                  {dept.categories.map((category) => (
                    <div
                      key={category.category}
                      className="flex justify-between items-center rounded-lg bg-white/5 p-3"
                    >
                      <span className="text-sm text-gray-300 truncate max-w-[120px]">
                        {category.category}
                      </span>
                      <span className="text-sm font-semibold text-cyan-400">
                        ${category.amount?.toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {financialsData?.length > 0 && (
        <div className="grid grid-cols-3 gap-4 mt-4">
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">
              Total {isDepartment ? "Departments" : "Segments"}
            </p>
            <p className="text-lg font-bold text-cyan-400">
              {financialsData.length}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Avg Amount</p>
            <p className="text-lg font-bold text-cyan-400">
              $
              {(
                financialsData.reduce(
                  (sum, item) => sum + item.total_amount,
                  0
                ) / financialsData.length
              )?.toLocaleString()}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Most Volatile</p>
            <p className="text-lg font-bold text-red-400">
              $
              {Math.max(
                ...financialsData.map((item) => item.amount_volatility || 0)
              )?.toLocaleString()}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
