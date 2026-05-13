import { BarChart3, Tag } from "lucide-react";

export default function CategoryPerformance({ data }) {
  const categories = data.category_performance || [];
  const maxRevenue = Math.max(
    ...categories.map((cat) => cat.total_revenue || 0)
  );

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-purple-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-purple-600">
            <BarChart3 className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Category Performance
          </span>
        </div>
        <span className="rounded-full bg-purple-600/20 px-4 py-1 text-sm font-medium text-purple-400">
          Categories
        </span>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-gray-300">
          <Tag className="h-5 w-5" />
          <span className="text-lg font-medium">
            {categories.length} Categories
          </span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      {categories.length > 0 && (
        <div className="space-y-4">
          {categories.map((category, index) => (
            <div
              key={category.category}
              className="group flex flex-col gap-3 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-purple-600/20 text-sm font-bold text-purple-400">
                    {index + 1}
                  </div>
                  <span className="font-semibold text-white group-hover:text-purple-300 transition-colors">
                    {category.category}
                  </span>
                </div>
                <span className="text-xl font-bold text-green-400">
                  ${category.total_revenue?.toLocaleString()}
                </span>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-400">
                <div className="flex gap-4">
                  <span>
                    {category.units_sold?.toLocaleString()} units sold
                  </span>
                  <span>${category.avg_price?.toFixed(2)} avg price</span>
                </div>
                <div className="flex gap-3">
                  <span className="text-green-400">
                    {category.revenue_share_percent}% revenue
                  </span>
                  <span className="text-blue-400">
                    {category.units_share_percent}% units
                  </span>
                </div>
              </div>

              <div className="flex gap-2">
                <div className="flex-1">
                  <div className="text-xs text-gray-500 mb-1">
                    Revenue Share
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                    <div
                      className="h-full rounded-full bg-green-500 transition-all duration-500"
                      style={{
                        width: `${Math.min(
                          (category.total_revenue / maxRevenue) * 100,
                          100
                        )}%`,
                      }}
                    />
                  </div>
                </div>
                <div className="flex-1">
                  <div className="text-xs text-gray-500 mb-1">Units Share</div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                    <div
                      className="h-full rounded-full bg-blue-500 transition-all duration-500"
                      style={{
                        width: `${category.units_share_percent}%`,
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {categories.length === 0 && (
        <div className="text-center py-8">
          <BarChart3 className="h-16 w-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">
            No category performance data available
          </p>
        </div>
      )}
    </div>
  );
}
