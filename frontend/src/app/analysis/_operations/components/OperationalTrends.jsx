import { TrendingUp } from "lucide-react";

export default function OperationalTrends({ data }) {
  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-pink-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-pink-600">
            <TrendingUp className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Operational Trends
          </span>
        </div>
        <span className="rounded-full bg-pink-600/20 px-4 py-1 text-sm font-medium text-pink-400">
          Analytics
        </span>
      </div>

      {data.growth_metrics && (
        <>
          <div className="flex items-end justify-between">
            <span
              className={`text-5xl font-extrabold ${
                data.growth_metrics.monthly_quantity_growth_percent >= 0
                  ? "text-green-400"
                  : "text-red-400"
              }`}
            >
              {data.growth_metrics.monthly_quantity_growth_percent >= 0
                ? "+"
                : ""}
              {data.growth_metrics?.monthly_quantity_growth_percent?.toFixed(1)}
              %
            </span>
            <div className="flex items-center text-xl font-semibold text-gray-400">
              <span className="mr-1">Monthly Growth</span>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />

          <div className="rounded-lg bg-gray-800 p-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Trend Direction</span>
              <span
                className={`text-lg font-bold ${
                  data.growth_metrics.trend_direction === "increasing"
                    ? "text-green-400"
                    : "text-red-400"
                }`}
              >
                {data.growth_metrics?.trend_direction?.charAt(0).toUpperCase() +
                  data.growth_metrics?.trend_direction?.slice(1)}
              </span>
            </div>
          </div>
        </>
      )}

      {data.monthly_operational_trends && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Monthly Trends
          </h3>
          <div className="space-y-3">
            {data.monthly_operational_trends?.slice(-6).map((month) => (
              <div
                key={month?.month}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {month?.month}
                  </span>
                  <span className="font-semibold text-pink-400">
                    {month.total_quantity?.toLocaleString()} units
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-400">Orders:</span>
                    <span className="ml-2 text-white font-medium">
                      {month.order_count?.toLocaleString()}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-400">Avg per Order:</span>
                    <span className="ml-2 text-white font-medium">
                      {month.avg_quantity_per_order?.toLocaleString()}
                    </span>
                  </div>
                  {month.total_cost && (
                    <>
                      <div>
                        <span className="text-gray-400">Total Cost:</span>
                        <span className="ml-2 text-green-400 font-medium">
                          ${month.total_cost?.toLocaleString()}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-400">Avg Cost:</span>
                        <span className="ml-2 text-green-400 font-medium">
                          ${month.avg_cost?.toLocaleString()}
                        </span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {data.weekly_patterns && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Weekly Patterns
          </h3>
          <div className="grid grid-cols-2 gap-3">
            {data.weekly_patterns?.map((day) => (
              <div
                key={day?.day}
                className="rounded-lg bg-gray-800 p-4 text-center"
              >
                <p className="text-sm text-gray-400">{day?.day}</p>
                <p className="text-lg font-bold text-pink-400">
                  {day.total_quantity?.toLocaleString()}
                </p>
                <p className="text-xs text-gray-500">
                  {day.order_count?.toLocaleString()} orders
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {data.seasonal_trends && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Seasonal Trends
          </h3>
          <div className="grid grid-cols-2 gap-4">
            {data.seasonal_trends?.map((season) => (
              <div
                key={season?.season}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="text-center">
                  <p className="text-sm text-gray-400 mb-1">{season?.season}</p>
                  <p className="text-xl font-bold text-pink-400">
                    {season.total_quantity?.toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500">
                    {season.order_count?.toLocaleString()} orders
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
