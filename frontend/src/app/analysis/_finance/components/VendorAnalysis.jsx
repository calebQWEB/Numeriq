import { Truck, Eye, EyeOff, Calendar } from "lucide-react";
import { useState } from "react";

export default function VendorAnalysis({ data }) {
  const [showAll, setShowAll] = useState(false);

  const displayVendors = showAll
    ? data.vendor_metrics
    : data.vendor_metrics?.slice(0, 5);

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-amber-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/10">
            <Truck className="h-6 w-6 text-amber-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              Vendor Analysis
            </h3>
            <p className="text-sm text-gray-400">
              Supplier and vendor performance metrics
            </p>
          </div>
        </div>
        {data.vendor_metrics?.length > 5 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="flex items-center gap-2 rounded-full border border-amber-500/30 bg-amber-500/10 px-4 py-2 text-sm font-medium text-amber-400 transition-colors hover:bg-amber-500/20"
          >
            {showAll ? (
              <>
                <EyeOff className="h-4 w-4" /> Show Less
              </>
            ) : (
              <>
                <Eye className="h-4 w-4" /> Show All
              </>
            )}
          </button>
        )}
      </div>

      <hr className="my-2 border-gray-700" />

      {data.vendor_concentration && (
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Top 5 Vendors</p>
            <p className="text-lg font-bold text-amber-400">
              {data.vendor_concentration.top_5_vendor_percentage?.toFixed(1)}%
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Total Vendors</p>
            <p className="text-lg font-bold text-amber-400">
              {data.vendor_concentration.vendor_diversity_index}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Avg Transaction</p>
            <p className="text-lg font-bold text-amber-400">
              $
              {data.vendor_concentration.average_vendor_transaction_value?.toLocaleString()}
            </p>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {displayVendors?.map((vendor, index) => (
          <div
            key={vendor.vendor}
            className="flex items-center justify-between rounded-xl bg-white/5 p-4 transition-colors duration-200 hover:bg-white/10"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-600 text-sm font-bold text-white shadow-md">
                {index + 1}
              </div>
              <div>
                <h4 className="font-semibold text-white truncate max-w-[200px]">
                  {vendor.vendor}
                </h4>
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  <span>
                    {vendor.percentage_of_total?.toFixed(1)}% of total
                  </span>
                  {vendor.relationship_duration_days && (
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      <span>{vendor.relationship_duration_days} days</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="text-right">
              <p className="font-bold text-amber-400">
                ${vendor.total_amount?.toLocaleString()}
              </p>
              <div className="text-sm text-gray-400">
                <p>{vendor.transaction_count} transactions</p>
                <p>Avg: ${vendor.average_transaction?.toLocaleString()}</p>
                {vendor.last_transaction_date && (
                  <p className="text-xs">
                    Last: {vendor.last_transaction_date}
                  </p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
