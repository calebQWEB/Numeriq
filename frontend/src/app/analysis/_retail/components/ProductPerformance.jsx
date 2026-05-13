import { TrendingUp, Package } from "lucide-react";

export default function ProductPerformance({ data }) {
  const topProducts =
    data.top_performing_products || data.top_selling_products || [];

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-blue-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-600">
            <TrendingUp className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Top Performing Products
          </span>
        </div>
        <span className="rounded-full bg-blue-600/20 px-4 py-1 text-sm font-medium text-blue-400">
          Performance
        </span>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-gray-300">
          <Package className="h-5 w-5" />
          <span className="text-lg font-medium">
            {topProducts.length} Top Products
          </span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      {topProducts.length > 0 && (
        <div className="space-y-4">
          {topProducts.slice(0, 8).map((product, index) => (
            <div
              key={product.product}
              className="group flex items-center justify-between rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-600/20 text-sm font-bold text-blue-400">
                  {index + 1}
                </div>
                <div className="flex flex-col">
                  <span className="font-semibold text-white group-hover:text-blue-300 transition-colors">
                    {product.product}
                  </span>
                  <span className="text-sm text-gray-400">
                    {product.transactions} transactions • {product.units_sold}{" "}
                    units
                  </span>
                </div>
              </div>
              <div className="text-right">
                {product.total_revenue ? (
                  <>
                    <span className="text-xl font-bold text-green-400">
                      ${product.total_revenue.toLocaleString()}
                    </span>
                    <div className="text-sm text-gray-400">
                      ${product.avg_price?.toFixed(2)} avg price
                    </div>
                  </>
                ) : (
                  <span className="text-xl font-bold text-blue-400">
                    {product.units_sold.toLocaleString()} units
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {topProducts.length === 0 && (
        <div className="text-center py-8">
          <Package className="h-16 w-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">No product performance data available</p>
        </div>
      )}
    </div>
  );
}
