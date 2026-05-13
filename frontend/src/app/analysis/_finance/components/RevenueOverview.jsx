import { DollarSign } from "lucide-react";

export default function RevenueOverview({ data }) {
  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-green-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-600">
            <DollarSign className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Total Revenue
          </span>
        </div>
        <span className="rounded-full bg-green-600/20 px-4 py-1 text-sm font-medium text-green-400">
          Overview
        </span>
      </div>

      <div className="flex items-end justify-between">
        <span className="text-5xl font-extrabold text-green-400">
          ${data.revenue_overview?.total_revenue?.toLocaleString()}
        </span>
        <div className="flex items-center text-xl font-semibold text-gray-400">
          <span className="mr-1">USD</span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Average Revenue</p>
          <p className="text-xl font-bold text-green-400">
            ${data.revenue_overview?.average_revenue?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Revenue Transactions</p>
          <p className="text-xl font-bold text-green-400">
            {data.revenue_overview?.revenue_transactions?.toLocaleString()}
          </p>
        </div>
      </div>

      {data.revenue_overview?.revenue_by_category && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Revenue By Category
          </h3>
          <ul className="mt-4 space-y-4">
            {data.revenue_by_category?.slice(0, 5).map((category) => (
              <li
                key={category?.category}
                className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {category?.category}
                  </span>
                  <span className="font-semibold text-white">
                    ${category.total_revenue?.toLocaleString()}
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-green-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(
                        (category.total_revenue / data.total_revenue) * 100,
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
