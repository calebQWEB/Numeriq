import { Tag, Eye, EyeOff } from "lucide-react";
import { useState } from "react";

export default function TransactionsByCategory({
  data,
  title = "Transactions by Category",
}) {
  const [showAll, setShowAll] = useState(false);

  // Determine which category data to use based on what's available
  const getCategoryData = () => {
    if (data.transactions_by_category)
      return { data: data.transactions_by_category, type: "category" };
    if (data.transactions_by_department)
      return { data: data.transactions_by_department, type: "department" };
    if (data.transactions_by_account)
      return { data: data.transactions_by_account, type: "account" };
    if (data.transactions_by_vendor)
      return { data: data.transactions_by_vendor, type: "vendor" };
    if (data.transactions_by_customer)
      return { data: data.transactions_by_customer, type: "customer" };
    return null;
  };

  const categoryInfo = getCategoryData();
  if (!categoryInfo) return null;

  const { data: categoryData, type } = categoryInfo;
  const displayItems = showAll ? categoryData : categoryData?.slice(0, 5);

  const getTitle = () => {
    if (title !== "Transactions by Category") return title;
    return `Transactions by ${type.charAt(0).toUpperCase() + type.slice(1)}`;
  };

  const getItemName = (item) => {
    return item[`${type}_name`] || item[type] || item.name;
  };

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-teal-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-teal-500/20 bg-teal-500/10">
            <Tag className="h-6 w-6 text-teal-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              {getTitle()}
            </h3>
            <p className="text-sm text-gray-400">
              Transaction breakdown and distribution
            </p>
          </div>
        </div>
        {categoryData?.length > 5 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="flex items-center gap-2 rounded-full border border-teal-500/30 bg-teal-500/10 px-4 py-2 text-sm font-medium text-teal-400 transition-colors hover:bg-teal-500/20"
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

      <div className="space-y-4">
        {displayItems?.map((item, index) => (
          <div
            key={getItemName(item)}
            className="flex items-center justify-between rounded-xl bg-white/5 p-4 transition-colors duration-200 hover:bg-white/10"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-teal-600 text-sm font-bold text-white shadow-md">
                {index + 1}
              </div>
              <div>
                <h4 className="font-semibold text-white truncate max-w-[250px]">
                  {getItemName(item)}
                </h4>
                <p className="text-sm text-gray-400">
                  {item.percentage_of_total?.toFixed(1)}% of total
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold text-teal-400">
                ${item.total_amount?.toLocaleString()}
              </p>
              <p className="text-sm text-gray-400">
                {item.transaction_count?.toLocaleString()} transactions
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
