import { Database, FileSpreadsheet, CheckCircle, BarChart } from "lucide-react";

export default function DatasetInfo({ data }) {
  const datasetInfo = data.dataset_info || {};
  const productMetrics = data.product_metrics || {};
  const categoryMetrics = data.category_metrics || {};
  const brandMetrics = data.brand_metrics || {};

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-slate-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-600">
            <Database className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Dataset Overview
          </span>
        </div>
        <span className="rounded-full bg-slate-600/20 px-4 py-1 text-sm font-medium text-slate-400">
          Analytics
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <div className="flex items-center gap-2 mb-2">
            <FileSpreadsheet className="h-5 w-5 text-blue-400" />
            <p className="text-sm text-gray-400">Total Records</p>
          </div>
          <p className="text-xl font-bold text-blue-400">
            {datasetInfo.total_records?.toLocaleString()}
          </p>
        </div>

        <div className="rounded-lg bg-gray-800 p-4">
          <div className="flex items-center gap-2 mb-2">
            <BarChart className="h-5 w-5 text-purple-400" />
            <p className="text-sm text-gray-400">Total Columns</p>
          </div>
          <p className="text-xl font-bold text-purple-400">
            {datasetInfo.total_columns}
          </p>
        </div>

        <div className="rounded-lg bg-gray-800 p-4">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="h-5 w-5 text-green-400" />
            <p className="text-sm text-gray-400">Columns Mapped</p>
          </div>
          <p className="text-xl font-bold text-green-400">
            {datasetInfo.columns_mapped}
          </p>
        </div>

        <div className="rounded-lg bg-gray-800 p-4">
          <div className="flex items-center gap-2 mb-2">
            <Database className="h-5 w-5 text-yellow-400" />
            <p className="text-sm text-gray-400">Data Quality</p>
          </div>
          <p className="text-xl font-bold text-yellow-400">
            {datasetInfo.data_completeness}%
          </p>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid md:grid-cols-3 gap-6">
        {/* Product Metrics */}
        {Object.keys(productMetrics).length > 0 && (
          <div className="rounded-lg bg-blue-900/20 border border-blue-500/30 p-4">
            <h3 className="text-lg font-semibold text-blue-300 mb-3">
              Product Diversity
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Unique Products</span>
                <span className="text-xl font-bold text-blue-400">
                  {productMetrics.unique_products?.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Avg Records/Product</span>
                <span className="text-lg font-semibold text-blue-300">
                  {productMetrics.avg_records_per_product}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Category Metrics */}
        {Object.keys(categoryMetrics).length > 0 && (
          <div className="rounded-lg bg-purple-900/20 border border-purple-500/30 p-4">
            <h3 className="text-lg font-semibold text-purple-300 mb-3">
              Category Spread
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Unique Categories</span>
                <span className="text-xl font-bold text-purple-400">
                  {categoryMetrics.unique_categories}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Brand Metrics */}
        {Object.keys(brandMetrics).length > 0 && (
          <div className="rounded-lg bg-pink-900/20 border border-pink-500/30 p-4">
            <h3 className="text-lg font-semibold text-pink-300 mb-3">
              Brand Portfolio
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Unique Brands</span>
                <span className="text-xl font-bold text-pink-400">
                  {brandMetrics.unique_brands}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Data Completeness Visualization */}
      <div className="rounded-lg bg-gray-800/50 border border-gray-700 p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-gray-300">
            Data Completeness
          </h3>
          <span className="text-sm text-gray-400">
            {datasetInfo.data_completeness}% Complete
          </span>
        </div>
        <div className="h-4 w-full overflow-hidden rounded-full bg-gray-700">
          <div
            className="h-full rounded-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 transition-all duration-1000"
            style={{
              width: `${datasetInfo.data_completeness}%`,
            }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-500 mt-2">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>
      </div>

      {/* Mapping Success Rate */}
      <div className="rounded-lg bg-gray-800/50 border border-gray-700 p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-gray-300">
            Column Mapping Success
          </h3>
          <span className="text-sm text-gray-400">
            {datasetInfo.columns_mapped} of {datasetInfo.total_columns} mapped
          </span>
        </div>
        <div className="h-4 w-full overflow-hidden rounded-full bg-gray-700">
          <div
            className="h-full rounded-full bg-gradient-to-r from-blue-500 to-green-500 transition-all duration-1000"
            style={{
              width: `${
                (datasetInfo.columns_mapped / datasetInfo.total_columns) * 100
              }%`,
            }}
          />
        </div>
        <div className="text-center mt-2 text-sm text-gray-400">
          {(
            (datasetInfo.columns_mapped / datasetInfo.total_columns) *
            100
          ).toFixed(1)}
          % of columns successfully mapped
        </div>
      </div>
    </div>
  );
}
