import { Target, TrendingUp, TrendingDown, Eye, EyeOff } from "lucide-react";
import { useState } from "react";

export default function BudgetVariance({ data }) {
  const [showCategories, setShowCategories] = useState(false);
  const budgetPerformance = data.budget_performance;
  const isOverBudget = budgetPerformance?.variance_percentage > 0;

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-orange-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-orange-500/20 bg-orange-500/10">
            <Target className="h-6 w-6 text-orange-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight text-white">
              Budget Variance Analysis
            </h3>
            <p className="text-sm text-gray-400">
              Budget vs actual performance
            </p>
          </div>
        </div>
        {data.budget_variance_by_category && (
          <button
            onClick={() => setShowCategories(!showCategories)}
            className="flex items-center gap-2 rounded-full border border-orange-500/30 bg-orange-500/10 px-4 py-2 text-sm font-medium text-orange-400 transition-colors hover:bg-orange-500/20"
          >
            {showCategories ? (
              <>
                <EyeOff className="h-4 w-4" /> Hide Categories
              </>
            ) : (
              <>
                <Eye className="h-4 w-4" /> Show Categories
              </>
            )}
          </button>
        )}
      </div>

      <hr className="my-2 border-gray-700" />

      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-xl bg-white/5 p-4 text-center">
          <p className="text-sm text-gray-400">Total Budget</p>
          <p className="text-xl font-bold text-blue-400">
            ${budgetPerformance?.total_budget?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-xl bg-white/5 p-4 text-center">
          <p className="text-sm text-gray-400">Total Actual</p>
          <p className="text-xl font-bold text-green-400">
            ${budgetPerformance?.total_actual?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-xl bg-white/5 p-4 text-center">
          <div className="flex justify-center mb-2">
            <div
              className={`h-8 w-8 rounded-full ${
                isOverBudget ? "bg-red-600" : "bg-green-600"
              } flex items-center justify-center`}
            >
              {isOverBudget ? (
                <TrendingUp className="h-4 w-4 text-white" />
              ) : (
                <TrendingDown className="h-4 w-4 text-white" />
              )}
            </div>
          </div>
          <p className="text-sm text-gray-400">Variance</p>
          <p
            className={`text-xl font-bold ${
              isOverBudget ? "text-red-400" : "text-green-400"
            }`}
          >
            {budgetPerformance?.variance_percentage?.toFixed(1)}%
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-4">
          <div className="rounded-lg bg-white/5 p-4">
            <p className="text-sm text-gray-400">Budget Utilization</p>
            <p className="text-lg font-bold text-blue-400">
              {budgetPerformance?.budget_utilization_rate?.toFixed(1)}%
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4">
            <p className="text-sm text-gray-400">Over Budget Items</p>
            <p className="text-lg font-bold text-red-400">
              {budgetPerformance?.over_budget_items?.toLocaleString()}
            </p>
          </div>
        </div>
        <div className="space-y-4">
          <div className="rounded-lg bg-white/5 p-4">
            <p className="text-sm text-gray-400">Under Budget Items</p>
            <p className="text-lg font-bold text-green-400">
              {budgetPerformance?.under_budget_items?.toLocaleString()}
            </p>
          </div>
          <div className="rounded-lg bg-white/5 p-4">
            <p className="text-sm text-gray-400">On Budget Items</p>
            <p className="text-lg font-bold text-blue-400">
              {budgetPerformance?.on_budget_items?.toLocaleString()}
            </p>
          </div>
        </div>
      </div>

      {showCategories && data.budget_variance_by_category && (
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-gray-300">
            Budget Variance by Category
          </h4>
          {data.budget_variance_by_category.map((category, index) => (
            <div
              key={category.category}
              className="flex items-center justify-between rounded-xl bg-white/5 p-4 transition-colors duration-200 hover:bg-white/10"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-orange-600 text-sm font-bold text-white shadow-md">
                  {index + 1}
                </div>
                <div>
                  <h4 className="font-semibold text-white">
                    {category.category}
                  </h4>
                  <p className="text-sm text-gray-400">
                    Utilization: {category.utilization_rate?.toFixed(1)}%
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p
                  className={`font-bold ${
                    category.variance >= 0 ? "text-red-400" : "text-green-400"
                  }`}
                >
                  ${Math.abs(category.variance)?.toLocaleString()}
                  <span className="text-sm ml-1">
                    ({category.variance_percentage?.toFixed(1)}%)
                  </span>
                </p>
                <p className="text-sm text-gray-400">
                  ${category.budgeted?.toLocaleString()} budgeted
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
