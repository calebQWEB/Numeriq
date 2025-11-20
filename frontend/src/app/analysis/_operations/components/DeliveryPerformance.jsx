import { Clock } from "lucide-react";

export default function DeliveryPerformance({ data }) {
  const deliveryData = data.delivery_performance;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-cyan-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-cyan-600">
            <Clock className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Delivery Performance
          </span>
        </div>
        <span className="rounded-full bg-cyan-600/20 px-4 py-1 text-sm font-medium text-cyan-400">
          Shipping
        </span>
      </div>

      {deliveryData?.on_time_delivery && (
        <>
          <div className="flex items-end justify-between">
            <span className="text-5xl font-extrabold text-cyan-400">
              {deliveryData.on_time_delivery?.on_time_delivery_rate_percent?.toFixed(
                1
              )}
              %
            </span>
            <div className="flex items-center text-xl font-semibold text-gray-400">
              <span className="mr-1">On-Time</span>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />
        </>
      )}

      <div className="grid grid-cols-2 gap-4">
        {deliveryData?.on_time_delivery && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Deliveries</p>
              <p className="text-xl font-bold text-cyan-400">
                {deliveryData.on_time_delivery?.total_deliveries?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">On-Time Deliveries</p>
              <p className="text-xl font-bold text-green-400">
                {deliveryData.on_time_delivery?.on_time_deliveries?.toLocaleString()}
              </p>
            </div>
          </>
        )}

        {deliveryData?.delivery_time_analysis && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Avg Delivery Time</p>
              <p className="text-xl font-bold text-cyan-400">
                {deliveryData.delivery_time_analysis?.avg_delivery_time_days?.toFixed(
                  1
                )}{" "}
                days
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Fastest Delivery</p>
              <p className="text-xl font-bold text-green-400">
                {deliveryData.delivery_time_analysis?.fastest_delivery_days?.toFixed(
                  1
                )}{" "}
                days
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Slowest Delivery</p>
              <p className="text-xl font-bold text-red-400">
                {deliveryData.delivery_time_analysis?.slowest_delivery_days?.toFixed(
                  1
                )}{" "}
                days
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Median Delivery Time</p>
              <p className="text-xl font-bold text-cyan-400">
                {deliveryData.delivery_time_analysis?.median_delivery_time_days?.toFixed(
                  1
                )}{" "}
                days
              </p>
            </div>
          </>
        )}
      </div>

      {deliveryData?.delivery_time_distribution && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Delivery Speed Distribution
          </h3>
          <ul className="mt-4 space-y-4">
            {deliveryData.delivery_time_distribution?.map((dist) => (
              <li
                key={dist?.category}
                className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {dist?.category} Delivery
                  </span>
                  <span className="font-semibold text-white">
                    {dist.delivery_count?.toLocaleString()} deliveries
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-cyan-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(
                        (dist.delivery_count /
                          deliveryData.on_time_delivery?.total_deliveries) *
                          100,
                        100
                      )}%`,
                    }}
                  />
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
