import { Truck } from "lucide-react";

export default function SupplyChainPerformance({ data }) {
  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-orange-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-orange-600">
            <Truck className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Supply Chain Performance
          </span>
        </div>
        <span className="rounded-full bg-orange-600/20 px-4 py-1 text-sm font-medium text-orange-400">
          Logistics
        </span>
      </div>

      {data.lead_time_metrics && (
        <>
          <div className="flex items-end justify-between">
            <span className="text-5xl font-extrabold text-orange-400">
              {data.lead_time_metrics?.avg_lead_time?.toFixed(1)}
            </span>
            <div className="flex items-center text-xl font-semibold text-gray-400">
              <span className="mr-1">Days</span>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />

          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Median Lead Time</p>
              <p className="text-xl font-bold text-orange-400">
                {data.lead_time_metrics?.median_lead_time?.toFixed(1)} days
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Consistency Score</p>
              <p className="text-xl font-bold text-orange-400">
                {data.lead_time_metrics?.lead_time_consistency_score?.toFixed(
                  1
                )}
                %
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Minimum Lead Time</p>
              <p className="text-xl font-bold text-green-400">
                {data.lead_time_metrics?.min_lead_time?.toFixed(1)} days
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Maximum Lead Time</p>
              <p className="text-xl font-bold text-red-400">
                {data.lead_time_metrics?.max_lead_time?.toFixed(1)} days
              </p>
            </div>
          </div>
        </>
      )}

      {data.supplier_performance && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Supplier Performance
          </h3>
          <ul className="mt-4 space-y-4">
            {data.supplier_performance?.slice(0, 5).map((supplier) => (
              <li
                key={supplier?.supplier}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {supplier?.supplier}
                  </span>
                  <span className="text-sm font-semibold text-white">
                    {supplier.order_count?.toLocaleString()} orders
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  {supplier.total_quantity && (
                    <div>
                      <span className="text-gray-400">Total Quantity:</span>
                      <span className="ml-2 text-white font-medium">
                        {supplier.total_quantity?.toLocaleString()}
                      </span>
                    </div>
                  )}

                  {supplier.avg_lead_time && (
                    <div>
                      <span className="text-gray-400">Avg Lead Time:</span>
                      <span className="ml-2 text-orange-400 font-medium">
                        {supplier.avg_lead_time?.toFixed(1)} days
                      </span>
                    </div>
                  )}

                  {supplier.total_cost && (
                    <div>
                      <span className="text-gray-400">Total Cost:</span>
                      <span className="ml-2 text-green-400 font-medium">
                        ${supplier.total_cost?.toLocaleString()}
                      </span>
                    </div>
                  )}

                  {supplier.lead_time_consistency && (
                    <div>
                      <span className="text-gray-400">Consistency:</span>
                      <span className="ml-2 text-blue-400 font-medium">
                        {supplier.lead_time_consistency?.toFixed(1)}
                      </span>
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
