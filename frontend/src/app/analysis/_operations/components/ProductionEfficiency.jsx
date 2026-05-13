import { Zap } from "lucide-react";

export default function ProductionEfficiency({ data }) {
  const prodData = data.production_efficiency;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-yellow-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-yellow-600">
            <Zap className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Production Efficiency
          </span>
        </div>
        <span className="rounded-full bg-yellow-600/20 px-4 py-1 text-sm font-medium text-yellow-400">
          Performance
        </span>
      </div>

      {prodData?.utilization && (
        <>
          <div className="flex items-end justify-between">
            <span className="text-5xl font-extrabold text-yellow-400">
              {prodData.utilization?.avg_utilization_percent?.toFixed(1)}%
            </span>
            <div className="flex items-center text-xl font-semibold text-gray-400">
              <span className="mr-1">Avg Utilization</span>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />
        </>
      )}

      <div className="grid grid-cols-2 gap-4">
        {prodData?.productivity && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Avg Productivity</p>
              <p className="text-xl font-bold text-yellow-400">
                {prodData.productivity?.avg_productivity?.toFixed(1)}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Max Productivity</p>
              <p className="text-xl font-bold text-green-400">
                {prodData.productivity?.max_productivity?.toFixed(1)}
              </p>
            </div>
          </>
        )}

        {prodData?.capacity && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Capacity</p>
              <p className="text-xl font-bold text-blue-400">
                {prodData.capacity?.total_capacity?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Avg Capacity</p>
              <p className="text-xl font-bold text-blue-400">
                {prodData.capacity?.avg_capacity?.toFixed(1)}
              </p>
            </div>
          </>
        )}

        {prodData?.downtime && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Downtime</p>
              <p className="text-xl font-bold text-red-400">
                {prodData.downtime?.total_downtime?.toFixed(1)}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Zero Downtime Periods</p>
              <p className="text-xl font-bold text-green-400">
                {prodData.downtime?.zero_downtime_periods?.toLocaleString()}
              </p>
            </div>
          </>
        )}
      </div>

      {prodData?.utilization && (
        <div className="rounded-lg bg-gray-800 p-4">
          <h3 className="text-lg font-semibold text-gray-300 mb-3">
            Utilization Analysis
          </h3>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="text-center">
              <span className="block text-gray-400">High Utilization</span>
              <span className="text-lg font-bold text-green-400">
                {prodData.utilization?.high_utilization_periods?.toLocaleString()}
              </span>
              <span className="block text-xs text-gray-500">≥90% periods</span>
            </div>
            <div className="text-center">
              <span className="block text-gray-400">Optimal Utilization</span>
              <span className="text-lg font-bold text-yellow-400">
                {prodData.utilization?.optimal_utilization_periods?.toLocaleString()}
              </span>
              <span className="block text-xs text-gray-500">
                75-90% periods
              </span>
            </div>
            <div className="text-center">
              <span className="block text-gray-400">Low Utilization</span>
              <span className="text-lg font-bold text-red-400">
                {prodData.utilization?.low_utilization_periods?.toLocaleString()}
              </span>
              <span className="block text-xs text-gray-500">≤50% periods</span>
            </div>
          </div>
        </div>
      )}

      {prodData?.productivity && (
        <div className="rounded-lg bg-gray-800 p-4">
          <h3 className="text-lg font-semibold text-gray-300 mb-3">
            Productivity Metrics
          </h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Median Productivity:</span>
              <span className="text-white font-medium">
                {prodData.productivity?.median_productivity?.toFixed(1)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Min Productivity:</span>
              <span className="text-white font-medium">
                {prodData.productivity?.min_productivity?.toFixed(1)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Productivity Std Dev:</span>
              <span className="text-white font-medium">
                {prodData.productivity?.productivity_std_dev?.toFixed(2)}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
