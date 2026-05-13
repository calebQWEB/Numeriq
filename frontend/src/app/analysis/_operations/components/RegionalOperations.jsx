import { MapPin } from "lucide-react";

export default function RegionalOperations({ data }) {
  const regionalData = data.regional_operations;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-indigo-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-600">
            <MapPin className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Regional Operations
          </span>
        </div>
        <span className="rounded-full bg-indigo-600/20 px-4 py-1 text-sm font-medium text-indigo-400">
          Geography
        </span>
      </div>

      {regionalData?.volume_by_region && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Volume by Region
          </h3>
          <ul className="space-y-4">
            {regionalData.volume_by_region?.slice(0, 8).map((region) => (
              <li
                key={region?.region}
                className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {region?.region}
                  </span>
                  <span className="font-semibold text-white">
                    {region.total_quantity?.toLocaleString()} units (
                    {region.percentage_of_total}%)
                  </span>
                </div>

                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-indigo-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(region.percentage_of_total, 100)}%`,
                    }}
                  />
                </div>

                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{region.order_count?.toLocaleString()} orders</span>
                  <span>
                    Avg: {region.avg_quantity_per_order?.toLocaleString()}{" "}
                    units/order
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {regionalData?.cost_by_region && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Cost by Region
          </h3>
          <ul className="space-y-4">
            {regionalData.cost_by_region?.slice(0, 8).map((region) => (
              <li
                key={region?.region}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {region?.region}
                  </span>
                  <span className="font-semibold text-green-400">
                    ${region.total_cost?.toLocaleString()}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-400">Average Cost:</span>
                    <span className="ml-2 text-white font-medium">
                      ${region.avg_cost?.toLocaleString()}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-400">Cost Variability:</span>
                    <span className="ml-2 text-yellow-400 font-medium">
                      ${region.cost_variability?.toFixed(2)}
                    </span>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
