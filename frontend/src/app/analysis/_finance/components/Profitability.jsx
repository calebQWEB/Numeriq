import { PieChart, TrendingUp } from "lucide-react";

export default function Profitability({ data }) {
  const profitMargin = data.profitability_overview.average_profit || 0;
  const profitabilityOverview = data.profitability_overview || {};
  const isPositive = profitMargin >= 0;

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-blue-500/20">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/10">
          <TrendingUp className="h-6 w-6 text-blue-400" />
        </div>
        <div>
          <h3 className="text-2xl font-bold tracking-tight text-white">
            Profitability Analysis
          </h3>
          <p className="text-sm text-gray-400">
            Financial performance overview
          </p>
        </div>
      </div>

      <hr className="my-2 border-gray-700" />

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-xl bg-white/5 p-4">
          <div className="flex items-center gap-3">
            <div
              className={`h-8 w-8 rounded-full ${
                isPositive ? "bg-green-600" : "bg-red-600"
              } flex items-center justify-center`}
            >
              <TrendingUp
                className={`h-4 w-4 ${
                  isPositive ? "text-white" : "text-white rotate-180"
                }`}
              />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Profit</p>
              <p
                className={`text-xl font-bold ${
                  isPositive ? "text-green-400" : "text-red-400"
                }`}
              >
                ${profitabilityOverview.total_profit?.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
        <div className="rounded-xl bg-white/5 p-4">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
              <PieChart className="h-4 w-4 text-white" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Avg Profit Margin</p>
              <p
                className={`text-xl font-bold ${
                  isPositive ? "text-green-400" : "text-red-400"
                }`}
              >
                {profitMargin.toFixed(2)}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {data.revenue_overview?.total_revenue && (
        <div className="space-y-4">
          <div className="flex items-center justify-between rounded-xl bg-white/5 p-4">
            <span className="font-medium text-gray-300">Total Revenue</span>
            <span className="font-bold text-green-400">
              ${data.revenue_overview?.total_revenue?.toLocaleString()}
            </span>
          </div>
          {/* <div className="flex items-center justify-between rounded-xl bg-white/5 p-4">
              <span className="font-medium text-gray-300">Total Expenses</span>
              <span className="font-bold text-red-400">
                ${data.expense_by_category?.total_expenses?.toLocaleString()}
              </span>
            </div> */}
        </div>
      )}

      {/* {data.monthly_profit_trends && (
        <div>
          <h4 className="text-lg font-semibold text-gray-300 mb-3">
            Monthly Profit Trends
          </h4>
          <div className="space-y-2">
            {data.monthly_profit_trends.slice(-6).map((trend) => (
              <div
                key={trend.month}
                className="flex items-center justify-between rounded-lg bg-white/5 p-3"
              >
                <span className="text-sm text-gray-400">{trend.month}</span>
                <span
                  className={`font-semibold ${
                    trend.profit >= 0 ? "text-green-400" : "text-red-400"
                  }`}
                >
                  ${trend.profit?.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )} */}
    </div>
  );
}
