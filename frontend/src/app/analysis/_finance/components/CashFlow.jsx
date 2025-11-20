import { Activity, ActivityIcon, TrendingDown, TrendingUp } from "lucide-react";

export default function CashFlow({ data }) {
  const cashFlowOverview = data.cashflow_overview || 0;
  const isPositive = cashFlowOverview >= 0;

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-purple-500/20">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-purple-500/20 bg-purple-500/10">
          <Activity className="h-6 w-6 text-purple-400" />
        </div>
        <div>
          <h3 className="text-2xl font-bold tracking-tight text-white">
            Cash Flow Analysis
          </h3>
          <p className="text-sm text-gray-400">Money in vs money out</p>
        </div>
      </div>

      <hr className="my-2 border-gray-700" />

      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-xl bg-white/5 p-4 text-center">
          <div className="flex justify-center mb-2">
            <div className="h-8 w-8 rounded-full bg-green-600 flex items-center justify-center">
              <TrendingUp className="h-4 w-4 text-white" />
            </div>
          </div>
          <p className="text-sm text-gray-400">Total Inflows</p>
          <p className="text-xl font-bold text-green-400">
            ${cashFlowOverview.total_inflows?.toLocaleString()}
          </p>
          <p className="text-xs text-gray-500">
            {cashFlowOverview.inflow_transactions} transactions
          </p>
        </div>

        <div className="rounded-xl bg-white/5 p-4 text-center">
          <div className="flex justify-center mb-2">
            <div className="h-8 w-8 rounded-full bg-red-600 flex items-center justify-center">
              <TrendingDown className="h-4 w-4 text-white" />
            </div>
          </div>
          <p className="text-sm text-gray-400">Total Outflows</p>
          <p className="text-xl font-bold text-red-400">
            ${cashFlowOverview.total_outflows?.toLocaleString()}
          </p>
          <p className="text-xs text-gray-500">
            {cashFlowOverview.outflow_transactions} transactions
          </p>
        </div>

        <div className="rounded-xl bg-white/5 p-4 text-center">
          <div className="flex justify-center mb-2">
            <div
              className={`h-8 w-8 rounded-full ${
                isPositive ? "bg-green-600" : "bg-red-600"
              } flex items-center justify-center`}
            >
              <ActivityIcon className="h-4 w-4 text-white" />
            </div>
          </div>
          <p className="text-sm text-gray-400">Net Cash Flow</p>
          <p
            className={`text-xl font-bold ${
              isPositive ? "text-green-400" : "text-red-400"
            }`}
          >
            ${Math.abs(cashFlowOverview.net_cashflow).toLocaleString()}
          </p>
          <p className="text-xs text-gray-500">
            {isPositive ? "Positive" : "Negative"}
          </p>
        </div>
      </div>

      {data.monthly_cashflow_trends && (
        <div>
          <h4 className="text-lg font-semibold text-gray-300 mb-3">
            Monthly Cash Flow Trends
          </h4>
          <div className="space-y-2">
            {data.monthly_cashflow_trends.slice(-6).map((trend) => (
              <div
                key={trend.month}
                className="flex items-center justify-between rounded-lg bg-white/5 p-3"
              >
                <span className="text-sm text-gray-400">{trend.month}</span>
                <span
                  className={`font-semibold ${
                    trend.net_cashflow >= 0 ? "text-green-400" : "text-red-400"
                  }`}
                >
                  ${Math.abs(trend.net_cashflow).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
