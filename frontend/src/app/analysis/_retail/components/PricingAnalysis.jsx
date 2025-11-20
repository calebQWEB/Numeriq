import { DollarSign, Percent, Target } from "lucide-react";

export default function PricingAnalysis({ data }) {
  const pricing = data.pricing_metrics || {};
  const margin = data.margin_analysis || {};
  const discount = data.discount_analysis || {};

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-emerald-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-600">
            <DollarSign className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Pricing Strategy
          </span>
        </div>
        <span className="rounded-full bg-emerald-600/20 px-4 py-1 text-sm font-medium text-emerald-400">
          Pricing
        </span>
      </div>

      {Object.keys(pricing).length > 0 && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Average Price</p>
              <p className="text-xl font-bold text-emerald-400">
                ${pricing.avg_selling_price?.toFixed(2)}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Median Price</p>
              <p className="text-xl font-bold text-emerald-400">
                ${pricing.median_price?.toFixed(2)}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Min Price</p>
              <p className="text-xl font-bold text-blue-400">
                ${pricing.price_range?.min?.toFixed(2)}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Max Price</p>
              <p className="text-xl font-bold text-purple-400">
                ${pricing.price_range?.max?.toFixed(2)}
              </p>
            </div>
          </div>

          <div className="rounded-lg bg-gray-800 p-4">
            <div className="flex items-center gap-2 mb-2">
              <Target className="h-5 w-5 text-gray-400" />
              <p className="text-sm text-gray-400">Price Variability</p>
            </div>
            <p className="text-lg font-bold text-yellow-400">
              ${pricing.price_std_dev?.toFixed(2)} Standard Deviation
            </p>
          </div>
        </>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Margin Analysis */}
        {Object.keys(margin).length > 0 && (
          <div className="rounded-lg bg-green-900/20 border border-green-500/30 p-4">
            <div className="flex items-center gap-2 mb-4">
              <Percent className="h-5 w-5 text-green-400" />
              <h3 className="text-lg font-semibold text-green-300">
                Margin Analysis
              </h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Average Margin</span>
                <span className="text-xl font-bold text-green-400">
                  {margin.avg_margin_percent?.toFixed(1)}%
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Median Margin</span>
                <span className="text-lg font-semibold text-green-300">
                  {margin.median_margin_percent?.toFixed(1)}%
                </span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Range</span>
                <span className="text-gray-300">
                  {margin.margin_range?.min?.toFixed(1)}% -{" "}
                  {margin.margin_range?.max?.toFixed(1)}%
                </span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700 mt-3">
                <div
                  className="h-full rounded-full bg-green-500 transition-all duration-500"
                  style={{
                    width: `${Math.min(margin.avg_margin_percent, 100)}%`,
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Discount Analysis */}
        {Object.keys(discount).length > 0 && (
          <div className="rounded-lg bg-orange-900/20 border border-orange-500/30 p-4">
            <div className="flex items-center gap-2 mb-4">
              <Target className="h-5 w-5 text-orange-400" />
              <h3 className="text-lg font-semibold text-orange-300">
                Discount Strategy
              </h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Average Discount</span>
                <span className="text-xl font-bold text-orange-400">
                  {discount.avg_discount_percent?.toFixed(1)}%
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Discounted Orders</span>
                <span className="text-lg font-semibold text-orange-300">
                  {discount.total_discount_transactions?.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Penetration Rate</span>
                <span className="text-gray-300">
                  {discount.discount_penetration?.toFixed(1)}%
                </span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700 mt-3">
                <div
                  className="h-full rounded-full bg-orange-500 transition-all duration-500"
                  style={{
                    width: `${discount.discount_penetration}%`,
                  }}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {Object.keys(pricing).length === 0 &&
        Object.keys(margin).length === 0 &&
        Object.keys(discount).length === 0 && (
          <div className="text-center py-8">
            <DollarSign className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">No pricing analysis data available</p>
          </div>
        )}
    </div>
  );
}
