import { Building2, TrendingUp } from "lucide-react";
import { useState } from "react";

export default function DepartmentMetrics({ data }) {
  const [activeTab, setActiveTab] = useState("salary");
  const departmentData = data.department_metrics;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-purple-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-purple-600">
            <Building2 className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Department Metrics
          </span>
        </div>
        <span className="rounded-full bg-purple-600/20 px-4 py-1 text-sm font-medium text-purple-400">
          Analysis
        </span>
      </div>

      <hr className="my-4 border-gray-700" />

      {/* Tab Navigation */}
      <div className="flex gap-2">
        {departmentData?.salary_by_department && (
          <button
            onClick={() => setActiveTab("salary")}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              activeTab === "salary"
                ? "bg-purple-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            Salary Metrics
          </button>
        )}
        {departmentData?.performance_by_department && (
          <button
            onClick={() => setActiveTab("performance")}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              activeTab === "performance"
                ? "bg-purple-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            Performance
          </button>
        )}
      </div>

      {/* Salary Tab */}
      {activeTab === "salary" && departmentData?.salary_by_department && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Salary by Department
          </h3>
          <div className="grid gap-4">
            {departmentData.salary_by_department?.map((dept) => (
              <div
                key={dept?.department}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-300 group-hover:text-white">
                    {dept?.department}
                  </span>
                  <span className="text-sm text-gray-400">
                    {dept?.employee_count} employees
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Average</p>
                    <p className="text-lg font-bold text-purple-400">
                      ${dept?.avg_salary?.toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Median</p>
                    <p className="text-lg font-bold text-purple-400">
                      ${dept?.median_salary?.toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Std Dev</p>
                    <p className="text-lg font-bold text-purple-400">
                      ${dept?.salary_std_dev?.toLocaleString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Performance Tab */}
      {activeTab === "performance" &&
        departmentData?.performance_by_department && (
          <div>
            <h3 className="text-xl font-semibold text-gray-300 mb-4">
              Performance by Department
            </h3>
            <div className="grid gap-4">
              {departmentData.performance_by_department?.map((dept) => (
                <div
                  key={dept?.department}
                  className="group flex items-center justify-between rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
                >
                  <div>
                    <span className="font-medium text-gray-300 group-hover:text-white">
                      {dept?.department}
                    </span>
                    <p className="text-sm text-gray-400">
                      {dept?.employees_rated} employees rated
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-purple-400" />
                    <span className="text-xl font-bold text-purple-400">
                      {dept?.avg_performance_rating?.toFixed(1)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
    </div>
  );
}
