import { Database } from "lucide-react";

export default function DatasetInfo({ data }) {
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
          Information
        </span>
      </div>

      <div className="flex items-end justify-between">
        <span className="text-5xl font-extrabold text-slate-400">
          {data.dataset_info?.total_records?.toLocaleString()}
        </span>
        <div className="flex items-center text-xl font-semibold text-gray-400">
          <span className="mr-1">Records</span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Total Columns</p>
          <p className="text-xl font-bold text-slate-400">
            {data.dataset_info?.total_columns?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Columns Mapped</p>
          <p className="text-xl font-bold text-blue-400">
            {data.dataset_info?.columns_mapped?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Data Completeness</p>
          <p className="text-xl font-bold text-green-400">
            {data.dataset_info?.data_completeness?.toFixed(1)}%
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Mapping Success</p>
          <p className="text-xl font-bold text-emerald-400">
            {(
              (data.dataset_info?.columns_mapped /
                data.dataset_info?.total_columns) *
              100
            )?.toFixed(1)}
            %
          </p>
        </div>
      </div>

      {data.diversity_metrics && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Data Diversity
          </h3>
          <div className="grid grid-cols-2 gap-4">
            {data.diversity_metrics?.unique_products && (
              <div className="rounded-lg bg-gray-800 p-4">
                <p className="text-sm text-gray-400">Unique Products</p>
                <p className="text-lg font-bold text-purple-400">
                  {data.diversity_metrics?.unique_products?.toLocaleString()}
                </p>
              </div>
            )}

            {data.diversity_metrics?.unique_suppliers && (
              <div className="rounded-lg bg-gray-800 p-4">
                <p className="text-sm text-gray-400">Unique Suppliers</p>
                <p className="text-lg font-bold text-orange-400">
                  {data.diversity_metrics?.unique_suppliers?.toLocaleString()}
                </p>
              </div>
            )}

            {data.diversity_metrics?.unique_warehouses && (
              <div className="rounded-lg bg-gray-800 p-4">
                <p className="text-sm text-gray-400">Unique Warehouses</p>
                <p className="text-lg font-bold text-cyan-400">
                  {data.diversity_metrics?.unique_warehouses?.toLocaleString()}
                </p>
              </div>
            )}

            {data.diversity_metrics?.unique_customers && (
              <div className="rounded-lg bg-gray-800 p-4">
                <p className="text-sm text-gray-400">Unique Customers</p>
                <p className="text-lg font-bold text-yellow-400">
                  {data.diversity_metrics?.unique_customers?.toLocaleString()}
                </p>
              </div>
            )}

            {data.diversity_metrics?.unique_regions && (
              <div className="rounded-lg bg-gray-800 p-4">
                <p className="text-sm text-gray-400">Unique Regions</p>
                <p className="text-lg font-bold text-indigo-400">
                  {data.diversity_metrics?.unique_regions?.toLocaleString()}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {data.volume_statistics && (
        <div className="rounded-lg bg-gray-800 p-4">
          <h3 className="text-lg font-semibold text-gray-300 mb-3">
            Volume Statistics
          </h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Total Volume:</span>
              <span className="text-white font-medium">
                {data.volume_statistics?.total_volume?.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Average per Record:</span>
              <span className="text-white font-medium">
                {data.volume_statistics?.avg_volume_per_record?.toFixed(1)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Median Volume:</span>
              <span className="text-white font-medium">
                {data.volume_statistics?.median_volume?.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Max Single Volume:</span>
              <span className="text-white font-medium">
                {data.volume_statistics?.max_single_volume?.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      )}

      {data.order_statistics && (
        <div className="rounded-lg bg-gray-800 p-4">
          <h3 className="text-lg font-semibold text-gray-300 mb-3">
            Order Statistics
          </h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Unique Orders:</span>
              <span className="text-white font-medium">
                {data.order_statistics?.unique_orders?.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Items per Order:</span>
              <span className="text-white font-medium">
                {data.order_statistics?.avg_items_per_order?.toFixed(1)}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
