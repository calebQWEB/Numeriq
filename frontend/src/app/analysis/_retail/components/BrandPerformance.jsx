import { Award, Star, TrendingUp } from "lucide-react";

export default function BrandPerformance({ data }) {
  const brands = data.brand_performance || [];
  const maxRevenue = Math.max(
    ...brands.map((brand) => brand.total_revenue || 0)
  );

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-pink-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-pink-600">
            <Award className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Brand Performance
          </span>
        </div>
        <span className="rounded-full bg-pink-600/20 px-4 py-1 text-sm font-medium text-pink-400">
          Brands
        </span>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-gray-300">
          <Star className="h-5 w-5" />
          <span className="text-lg font-medium">
            {brands.length} Active Brands
          </span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      {brands.length > 0 && (
        <div className="space-y-4">
          {brands.map((brand, index) => (
            <div
              key={brand.brand}
              className="group flex flex-col gap-3 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-pink-600/20 text-sm font-bold text-pink-400">
                    {index + 1}
                  </div>
                  <div className="flex flex-col">
                    <span className="font-semibold text-white group-hover:text-pink-300 transition-colors">
                      {brand.brand}
                    </span>
                    <span className="text-sm text-gray-400">
                      {brand.units_sold?.toLocaleString()} units sold
                    </span>
                  </div>
                </div>
                <span className="text-2xl font-bold text-green-400">
                  ${brand.total_revenue?.toLocaleString()}
                </span>
              </div>

              <div className="grid grid-cols-3 gap-4 text-sm">
                <div className="text-center">
                  <div className="text-gray-400 mb-1">Average Price</div>
                  <div className="text-lg font-bold text-blue-400">
                    ${brand.avg_price?.toFixed(2)}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-gray-400 mb-1">Price Consistency</div>
                  <div className="text-lg font-bold text-yellow-400">
                    ${brand.price_consistency?.toFixed(2)}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-gray-400 mb-1">Market Share</div>
                  <div className="text-lg font-bold text-purple-400">
                    {((brand.total_revenue / maxRevenue) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Revenue Performance</span>
                  <span>
                    {((brand.total_revenue / maxRevenue) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-pink-500 to-purple-500 transition-all duration-500"
                    style={{
                      width: `${(brand.total_revenue / maxRevenue) * 100}%`,
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {brands.length > 0 && (
        <div className="rounded-lg bg-gray-800/50 border border-gray-700 p-4">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="h-5 w-5 text-pink-400" />
            <h3 className="text-lg font-semibold text-pink-300">
              Brand Insights
            </h3>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="text-center">
              <div className="text-gray-400 mb-1">Top Brand</div>
              <div className="font-bold text-pink-400">{brands[0]?.brand}</div>
            </div>
            <div className="text-center">
              <div className="text-gray-400 mb-1">Highest Price</div>
              <div className="font-bold text-blue-400">
                ${Math.max(...brands.map((b) => b.avg_price || 0)).toFixed(2)}
              </div>
            </div>
            <div className="text-center">
              <div className="text-gray-400 mb-1">Most Consistent</div>
              <div className="font-bold text-yellow-400">
                {
                  brands.reduce((min, brand) =>
                    (brand.price_consistency || Infinity) <
                    (min.price_consistency || Infinity)
                      ? brand
                      : min
                  ).brand
                }
              </div>
            </div>
            <div className="text-center">
              <div className="text-gray-400 mb-1">Total Revenue</div>
              <div className="font-bold text-green-400">
                $
                {brands
                  .reduce((sum, brand) => sum + (brand.total_revenue || 0), 0)
                  .toLocaleString()}
              </div>
            </div>
          </div>
        </div>
      )}

      {brands.length === 0 && (
        <div className="text-center py-8">
          <Award className="h-16 w-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">No brand performance data available</p>
        </div>
      )}
    </div>
  );
}
