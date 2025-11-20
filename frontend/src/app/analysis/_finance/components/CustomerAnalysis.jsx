import { Users, Eye, EyeOff, Calendar, Clock } from "lucide-react";
import { useState } from "react";

export default function CustomerAnalysis({ data }) {
  const [showAll, setShowAll] = useState(false);

  const displayCustomers = showAll
    ? data.customer_metrics
    : data.customer_metrics?.slice(0, 5);

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-emerald-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/10">
            <Users className="h-6 w-6 text-emerald-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              Customer Analysis
            </h3>
            <p className="text-sm text-gray-400">
              Customer performance and relationship metrics
            </p>
          </div>
        </div>
        {data.customer_metrics?.length > 5 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 text-sm font-medium text-emerald-400 transition-colors hover:bg-emerald-500/20"
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

      {data.customer_concentration && (
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Top 5 Customers</p>
            <p className="text-lg font-bold text-emerald-400">
              {data.customer_concentration.top_5_customer_percentage?.toFixed(
                1
              )}
              %
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Total Customers</p>
            <p className="text-lg font-bold text-emerald-400">
              {data.customer_concentration.customer_diversity_index}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Avg Transaction</p>
            <p className="text-lg font-bold text-emerald-400">
              $
              {data.customer_concentration.average_customer_transaction_value?.toLocaleString()}
            </p>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {displayCustomers?.map((customer, index) => (
          <div
            key={customer.customer}
            className="flex items-center justify-between rounded-xl bg-white/5 p-4 transition-colors duration-200 hover:bg-white/10"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-600 text-sm font-bold text-white shadow-md">
                {index + 1}
              </div>
              <div>
                <h4 className="font-semibold text-white truncate max-w-[200px]">
                  {customer.customer}
                </h4>
                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <span>
                    {customer.percentage_of_total?.toFixed(1)}% of total
                  </span>
                  {customer.customer_lifetime_days && (
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      <span>{customer.customer_lifetime_days} days</span>
                    </div>
                  )}
                  {customer.transaction_frequency_days && (
                    <div className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      <span>
                        Every {customer.transaction_frequency_days} days
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="text-right">
              <p className="font-bold text-emerald-400">
                ${customer.total_amount?.toLocaleString()}
              </p>
              <div className="text-sm text-gray-400">
                <p>{customer.transaction_count} transactions</p>
                <p>Avg: ${customer.average_transaction?.toLocaleString()}</p>
                {customer.last_transaction_date && (
                  <p className="text-xs">
                    Last: {customer.last_transaction_date}
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
