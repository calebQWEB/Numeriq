import { Eye, EyeOff, TrendingDown } from "lucide-react";

export default function ExpenseAnalysis({ data }) {
  const [showAll, setShowAll] = useState(false);
  const displayCategories = showAll
    ? data.expense_by_category
    : data.expense_by_category?.slice(0, 5);

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-red-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/10">
            <TrendingDown className="h-6 w-6 text-red-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              Expense Analysis
            </h3>
            <p className="text-sm text-gray-400">
              Total expenses: ${data.total_expenses?.toLocaleString()}
            </p>
          </div>
        </div>
        {data.expense_by_category?.length > 5 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="flex items-center gap-2 rounded-full border border-red-500/30 bg-red-500/10 px-4 py-2 text-sm font-medium text-red-400 transition-colors hover:bg-red-500/20"
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

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="rounded-lg bg-white/5 p-4">
          <p className="text-sm text-gray-400">Average Expense</p>
          <p className="text-lg font-bold text-red-400">
            ${data.average_expense?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-white/5 p-4">
          <p className="text-sm text-gray-400">Largest Expense</p>
          <p className="text-lg font-bold text-red-400">
            ${data.largest_expense?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-white/5 p-4">
          <p className="text-sm text-gray-400">Total Transactions</p>
          <p className="text-lg font-bold text-red-400">
            {data.expense_transactions?.toLocaleString()}
          </p>
        </div>
      </div>

      {displayCategories && (
        <div className="space-y-4">
          {displayCategories.map((category, index) => (
            <div
              key={category.category}
              className="flex items-center justify-between rounded-xl bg-white/5 p-4 transition-colors duration-200 hover:bg-white/10"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-red-600 text-sm font-bold text-white shadow-md">
                  {index + 1}
                </div>
                <div>
                  <h4 className="font-semibold text-white">
                    {category.category}
                  </h4>
                  <p className="text-sm text-gray-400">
                    {category.percentage_of_total}% of total
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-bold text-red-400">
                  ${category.total_expense?.toLocaleString()}
                </p>
                <p className="text-sm text-gray-400">
                  {category.transaction_count} transactions
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
