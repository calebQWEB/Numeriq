import { Target, TrendingUp, TrendingDown } from "lucide-react";

export default function PerformanceMetrics({ data }) {
  const performanceData = data.performance_overview;
  const distributionData = data.performance_distribution;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-amber-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-amber-600">
            <Target className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Performance Metrics
          </span>
        </div>
        <span className="rounded-full bg-amber-600/20 px-4 py-1 text-sm font-medium text-amber-400">
          Ratings
        </span>
      </div>

      <div className="flex items-end justify-between">
        <span className="text-5xl font-extrabold text-amber-400">
          {performanceData?.avg_performance_rating?.toFixed(1)}
        </span>
        <div className="flex items-center text-xl font-semibold text-gray-400">
          <span className="mr-1">Average Rating</span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Median Rating</p>
          <p className="text-xl font-bold text-amber-400">
            {performanceData?.median_performance_rating?.toFixed(1)}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4 flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-400">High Performers</p>
            <p className="text-xl font-bold text-green-400">
              {performanceData?.high_performers}
            </p>
          </div>
          <TrendingUp className="h-6 w-6 text-green-400" />
        </div>
        <div className="rounded-lg bg-gray-800 p-4 flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-400">Low Performers</p>
            <p className="text-xl font-bold text-red-400">
              {performanceData?.low_performers}
            </p>
          </div>
          <TrendingDown className="h-6 w-6 text-red-400" />
        </div>
      </div>

      {distributionData && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Performance Distribution
          </h3>
          <div className="space-y-4">
            {distributionData?.map((category) => {
              const getColorClass = (cat) => {
                switch (cat.toLowerCase()) {
                  case "excellent":
                    return "bg-green-500";
                  case "good":
                    return "bg-blue-500";
                  case "average":
                    return "bg-yellow-500";
                  case "below average":
                    return "bg-orange-500";
                  case "poor":
                    return "bg-red-500";
                  default:
                    return "bg-gray-500";
                }
              };

              const getTextColor = (cat) => {
                switch (cat.toLowerCase()) {
                  case "excellent":
                    return "text-green-400";
                  case "good":
                    return "text-blue-400";
                  case "average":
                    return "text-yellow-400";
                  case "below average":
                    return "text-orange-400";
                  case "poor":
                    return "text-red-400";
                  default:
                    return "text-gray-400";
                }
              };

              const maxCount = Math.max(
                ...(distributionData?.map((d) => d.employee_count) || [1])
              );

              return (
                <div
                  key={category?.category}
                  className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
                >
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium text-gray-400 group-hover:text-gray-200">
                      {category?.category}
                    </span>
                    <span
                      className={`font-semibold ${getTextColor(
                        category?.category
                      )}`}
                    >
                      {category?.employee_count} employees
                    </span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                    <div
                      className={`h-full rounded-full ${getColorClass(
                        category?.category
                      )} transition-all duration-500`}
                      style={{
                        width: `${
                          (category?.employee_count / maxCount) * 100
                        }%`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
