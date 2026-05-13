import { Calendar, Snowflake, Flower, Sun, Leaf } from "lucide-react";

export default function SeasonalTrends({ data }) {
  const trends = data.seasonal_trends || [];

  const seasonIcons = {
    Winter: Snowflake,
    Spring: Flower,
    Summer: Sun,
    Fall: Leaf,
  };

  const seasonColors = {
    Winter: "text-blue-400 bg-blue-900/20 border-blue-700/30",
    Spring: "text-green-400 bg-green-900/20 border-green-700/30",
    Summer: "text-yellow-400 bg-yellow-900/20 border-yellow-700/30",
    Fall: "text-orange-400 bg-orange-900/20 border-orange-700/30",
  };

  const maxRevenue = Math.max(...trends.map((t) => t.total_revenue || 0));

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-teal-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-teal-600">
            <Calendar className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Seasonal Trends
          </span>
        </div>
        <span className="rounded-full bg-teal-600/20 px-4 py-1 text-sm font-medium text-teal-400">
          Seasonality
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {trends.map((trend, index) => {
          const IconComponent = seasonIcons[trend.season];
          const colorClasses = seasonColors[trend.season];

          return (
            <div
              key={trend.season}
              className={`group rounded-xl p-6 border transition-all duration-200 hover:scale-[1.02] ${colorClasses}`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  {IconComponent && (
                    <IconComponent
                      className={`h-6 w-6 ${colorClasses.split(" ")[0]}`}
                    />
                  )}
                  <h3
                    className={`text-xl font-semibold ${
                      colorClasses.split(" ")[0]
                    }`}
                  >
                    {trend.season}
                  </h3>
                </div>
                <span className="text-sm font-medium text-gray-400">
                  #{index + 1}
                </span>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Total Revenue</span>
                  <span
                    className={`text-2xl font-bold ${
                      colorClasses.split(" ")[0]
                    }`}
                  >
                    ${trend.total_revenue?.toLocaleString()}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Units Sold</span>
                  <span className="text-lg font-semibold text-white">
                    {trend.units_sold?.toLocaleString()}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Revenue Share</span>
                  <span className="text-sm font-medium text-gray-400">
                    {(
                      (trend.total_revenue /
                        trends.reduce((sum, t) => sum + t.total_revenue, 0)) *
                      100
                    ).toFixed(1)}
                    %
                  </span>
                </div>
              </div>

              {/* Performance indicator bar */}
              <div className="mt-4">
                <div className="flex justify-between text-xs text-gray-400 mb-1">
                  <span>Performance vs Peak Season</span>
                  <span>
                    {((trend.total_revenue / maxRevenue) * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      trend.season === "Winter"
                        ? "bg-blue-500"
                        : trend.season === "Spring"
                        ? "bg-green-500"
                        : trend.season === "Summer"
                        ? "bg-yellow-500"
                        : "bg-orange-500"
                    }`}
                    style={{
                      width: `${Math.min(
                        (trend.total_revenue / maxRevenue) * 100,
                        100
                      )}%`,
                    }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Seasonal Summary */}
      <div className="rounded-lg bg-gray-800 p-6">
        <h3 className="text-lg font-semibold text-gray-300 mb-4">
          Seasonal Performance Summary
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 rounded bg-gray-700">
            <span className="text-gray-400 block text-sm">Peak Season</span>
            <span className="text-lg font-semibold text-teal-400">
              {
                trends.reduce(
                  (max, trend) =>
                    trend.total_revenue > max.total_revenue ? trend : max,
                  trends[0]
                )?.season
              }
            </span>
          </div>

          <div className="p-3 rounded bg-gray-700">
            <span className="text-gray-400 block text-sm">Low Season</span>
            <span className="text-lg font-semibold text-gray-300">
              {
                trends.reduce(
                  (min, trend) =>
                    trend.total_revenue < min.total_revenue ? trend : min,
                  trends[0]
                )?.season
              }
            </span>
          </div>

          <div className="p-3 rounded bg-gray-700">
            <span className="text-gray-400 block text-sm">Total Revenue</span>
            <span className="text-lg font-semibold text-white">
              $
              {trends
                .reduce((sum, trend) => sum + trend.total_revenue, 0)
                .toLocaleString()}
            </span>
          </div>

          <div className="p-3 rounded bg-gray-700">
            <span className="text-gray-400 block text-sm">Seasonality</span>
            <span className="text-lg font-semibold text-white">
              {maxRevenue / Math.min(...trends.map((t) => t.total_revenue)) > 2
                ? "High"
                : "Moderate"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
