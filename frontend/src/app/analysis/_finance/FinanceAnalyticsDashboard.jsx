import AccountPerformance from "./components/AccountPerformance";
import BudgetVariance from "./components/BudgetVariance";
import CashFlow from "./components/CashFlow";
import CustomerAnalysis from "./components/CustomerAnalysis";
import DatasetInfo from "./components/DatasetInfo";
import DepartmentPerformance from "./components/DepartmentPerformance";
import ExpenseAnalysis from "./components/ExpenseAnalysis";
import FinancialTrends from "./components/FinancialTrends";
import Profitability from "./components/Profitability";
import RevenueOverview from "./components/RevenueOverview";
import TransactionsByCategory from "./components/TransactionsByCategory";
import TransactionSummary from "./components/TransactionSummary";
import VendorAnalysis from "./components/VendorAnalysis";

export default function FinanceAnalyticsDashboard({ analysis }) {
  return (
    <>
      {analysis && (
        <div>
          {/* Dataset Information */}
          {analysis.dataset_info && <DatasetInfo data={analysis} />}

          {/* Transaction Summary */}
          {analysis.transaction_summary && (
            <TransactionSummary data={analysis} />
          )}

          {/* Revenue Overview */}
          {analysis.revenue_overview && <RevenueOverview data={analysis} />}

          {/* Expense Analysis */}
          {analysis.expense_overview && <ExpenseAnalysis data={analysis} />}

          {/* Profitability */}
          {analysis.profitability_overview && <Profitability data={analysis} />}

          {/* Cash Flow */}
          {analysis.cashflow_overview && <CashFlow data={analysis} />}

          {/* Budget Performance */}
          {analysis.budget_performance && <BudgetVariance data={analysis} />}

          {/* Account Performance */}
          {analysis.account_performance && (
            <AccountPerformance data={analysis} />
          )}

          {/* Department Performance */}
          {(analysis.department_financials || analysis.segment_financials) && (
            <DepartmentPerformance data={analysis} />
          )}

          {/* Vendor Analysis */}
          {analysis.vendor_metrics && <VendorAnalysis data={analysis} />}

          {/* Customer Analysis */}
          {analysis.customer_metrics && <CustomerAnalysis data={analysis} />}

          {/* Financial Trends */}
          {(analysis.monthly_financial_trends ||
            analysis.quarterly_trends ||
            analysis.yearly_trends ||
            analysis.day_of_week_patterns) && (
            <FinancialTrends data={analysis} />
          )}

          {/* Transactions by Category/Department/Account/Vendor/Customer */}
          {(analysis.transactions_by_category ||
            analysis.transactions_by_department ||
            analysis.transactions_by_account ||
            analysis.transactions_by_vendor ||
            analysis.transactions_by_customer) && (
            <TransactionsByCategory data={analysis} />
          )}
        </div>
      )}
    </>
  );
}
