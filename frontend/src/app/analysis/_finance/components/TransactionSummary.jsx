import { Receipt, Eye, EyeOff } from "lucide-react";
import { useState } from "react";

export default function TransactionSummary({ data }) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-blue-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/10">
            <Receipt className="h-6 w-6 text-blue-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              Transaction Overview
            </h3>
            <p className="text-sm text-gray-400">
              {data.transaction_summary?.total_transactions?.toLocaleString()}{" "}
              total transactions
            </p>
          </div>
        </div>
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-2 text-sm font-medium text-blue-400 transition-colors hover:bg-blue-500/20"
        >
          {showDetails ? (
            <>
              <EyeOff className="h-4 w-4" /> Hide Details
            </>
          ) : (
            <>
              <Eye className="h-4 w-4" /> Show Details
            </>
          )}
        </button>
      </div>

      <hr className="my-2 border-gray-700" />

      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-xl bg-white/5 p-4 text-center">
          <p className="text-sm text-gray-400">Total Value</p>
          <p className="text-xl font-bold text-blue-400">
            ${data.transaction_summary?.total_amount?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-xl bg-white/5 p-4 text-center">
          <p className="text-sm text-gray-400">Average Transaction</p>
          <p className="text-xl font-bold text-blue-400">
            ${data.transaction_summary?.average_transaction?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-xl bg-white/5 p-4 text-center">
          <p className="text-sm text-gray-400">Median Transaction</p>
          <p className="text-xl font-bold text-blue-400">
            ${data.transaction_summary?.median_transaction?.toLocaleString()}
          </p>
        </div>
      </div>

      {showDetails && (
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-4">
            <div className="rounded-lg bg-white/5 p-4">
              <p className="text-sm text-gray-400">Largest Transaction</p>
              <p className="text-lg font-bold text-green-400">
                $
                {data.transaction_summary?.largest_transaction?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-white/5 p-4">
              <p className="text-sm text-gray-400">Positive Transactions</p>
              <p className="text-lg font-bold text-green-400">
                {data.transaction_summary?.positive_transactions?.toLocaleString()}
              </p>
            </div>
          </div>
          <div className="space-y-4">
            <div className="rounded-lg bg-white/5 p-4">
              <p className="text-sm text-gray-400">Smallest Transaction</p>
              <p className="text-lg font-bold text-blue-400">
                $
                {data.transaction_summary?.smallest_transaction?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-white/5 p-4">
              <p className="text-sm text-gray-400">Negative Transactions</p>
              <p className="text-lg font-bold text-red-400">
                {data.transaction_summary?.negative_transactions?.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
