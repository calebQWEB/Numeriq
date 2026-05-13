import { Package } from "lucide-react";

export default function OrderOverview({ data }) {
  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-blue-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-600">
            <Package className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Order Overview
          </span>
        </div>
        <span className="rounded-full bg-blue-600/20 px-4 py-1 text-sm font-medium text-blue-400">
          Operations
        </span>
      </div>

      <div className="flex items-end justify-between">
        <span className="text-5xl font-extrabold text-blue-400">
          {data.order_overview?.total_orders?.toLocaleString()}
        </span>
        <div className="flex items-center text-xl font-semibold text-gray-400">
          <span className="mr-1">Orders</span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Total Quantity</p>
          <p className="text-xl font-bold text-blue-400">
            {data.order_overview?.total_quantity_ordered?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Average Order Size</p>
          <p className="text-xl font-bold text-blue-400">
            {data.order_overview?.average_order_quantity?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Largest Order</p>
          <p className="text-xl font-bold text-blue-400">
            {data.order_overview?.largest_order?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Smallest Order</p>
          <p className="text-xl font-bold text-blue-400">
            {data.order_overview?.smallest_order?.toLocaleString()}
          </p>
        </div>
      </div>

      {data.order_status_breakdown && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Order Status Breakdown
          </h3>
          <ul className="mt-4 space-y-4">
            {data.order_status_breakdown?.slice(0, 5).map((status) => (
              <li
                key={status?.status}
                className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {status?.status}
                  </span>
                  <span className="font-semibold text-white">
                    {status.order_count?.toLocaleString()} ({status.percentage}
                    %)
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-blue-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(status.percentage, 100)}%`,
                    }}
                  />
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.fulfillment_metrics && (
        <div className="rounded-lg bg-gray-800 p-4">
          <h3 className="text-lg font-semibold text-gray-300 mb-3">
            Fulfillment Performance
          </h3>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-400">Fulfillment Rate</span>
            <span className="text-lg font-bold text-green-400">
              {data.fulfillment_metrics?.fulfillment_rate_percent}%
            </span>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm text-gray-400">Completed Orders</span>
            <span className="text-sm font-medium text-white">
              {data.fulfillment_metrics?.completed_orders?.toLocaleString()}
            </span>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm text-gray-400">Pending Orders</span>
            <span className="text-sm font-medium text-white">
              {data.fulfillment_metrics?.pending_orders?.toLocaleString()}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
