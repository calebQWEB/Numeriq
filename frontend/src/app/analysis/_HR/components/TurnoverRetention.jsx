import { RotateCcw, Calendar, TrendingDown } from "lucide-react";

export default function TurnoverRetention({ data }) {
  const turnoverData = data.turnover_retention_metrics;

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-red-500/20">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/10">
          <RotateCcw className="h-6 w-6 text-red-400" />
        </div>
        <div>
          <h3 className="text-2xl font-bold tracking-tight text-white">
            Turnover & Retention
          </h3>
          <p className="text-sm text-gray-400">
            Employee retention and turnover insights
          </p>
        </div>
      </div>

      <hr className="my-2 border-gray-700" />

      {turnoverData?.tenure_analysis && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="rounded-xl bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Average Tenure</p>
            <p className="text-xl font-bold text-blue-400">
              {turnoverData.tenure_analysis.avg_tenure_years?.toFixed(1)} years
            </p>
          </div>
          <div className="rounded-xl bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Median Tenure</p>
            <p className="text-xl font-bold text-green-400">
              {turnoverData.tenure_analysis.median_tenure_years?.toFixed(1)}{" "}
              years
            </p>
          </div>
          <div className="rounded-xl bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Max Tenure</p>
            <p className="text-xl font-bold text-purple-400">
              {turnoverData.tenure_analysis.max_tenure_years?.toFixed(1)} years
            </p>
          </div>
          <div className="rounded-xl bg-white/5 p-4 text-center">
            <p className="text-sm text-gray-400">Min Tenure</p>
            <p className="text-xl font-bold text-yellow-400">
              {turnoverData.tenure_analysis.min_tenure_years?.toFixed(1)} years
            </p>
          </div>
        </div>
      )}

      {turnoverData?.termination_analysis && (
        <div>
          <h4 className="text-lg font-semibold text-gray-300 mb-3 flex items-center gap-2">
            <TrendingDown className="h-5 w-5 text-red-400" />
            Termination Analysis
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="rounded-xl bg-red-500/10 border border-red-500/20 p-4">
              <p className="text-sm text-gray-400">Annual Turnover Rate</p>
              <p className="text-xl font-bold text-red-400">
                {turnoverData.termination_analysis.annual_turnover_rate}%
              </p>
            </div>
            <div className="rounded-xl bg-white/5 p-4">
              <p className="text-sm text-gray-400">Terminations Last Year</p>
              <p className="text-xl font-bold text-orange-400">
                {turnoverData.termination_analysis.terminations_last_year?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-xl bg-white/5 p-4">
              <p className="text-sm text-gray-400">Monthly Avg</p>
              <p className="text-xl font-bold text-yellow-400">
                {turnoverData.termination_analysis.monthly_avg_terminations?.toFixed(
                  1
                )}
              </p>
            </div>
          </div>
        </div>
      )}

      {turnoverData?.tenure_distribution && (
        <div>
          <h4 className="text-lg font-semibold text-gray-300 mb-3">
            Tenure Distribution
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {turnoverData.tenure_distribution.map((band) => (
              <div key={band.tenure_band} className="rounded-lg bg-white/5 p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-300">
                    {band.tenure_band}
                  </span>
                  <span className="text-sm text-blue-400 font-semibold">
                    {band.employee_count}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-500">
                    {band.percentage}%
                  </span>
                  <div className="flex-1 mx-2">
                    <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                      <div
                        className="h-full rounded-full bg-blue-500 transition-all duration-500"
                        style={{ width: `${Math.min(band.percentage, 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {turnoverData?.new_hire_metrics && (
        <div>
          <h4 className="text-lg font-semibold text-gray-300 mb-3 flex items-center gap-2">
            <Calendar className="h-5 w-5 text-green-400" />
            New Hire Metrics
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="rounded-lg bg-green-500/10 border border-green-500/20 p-4">
              <p className="text-sm text-gray-400">New Hires (Last Year)</p>
              <p className="text-lg font-bold text-green-400">
                {turnoverData.new_hire_metrics.new_hires_last_year?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-blue-500/10 border border-blue-500/20 p-4">
              <p className="text-sm text-gray-400">New Hires (6 Months)</p>
              <p className="text-lg font-bold text-blue-400">
                {turnoverData.new_hire_metrics.new_hires_last_6_months?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-white/5 p-4">
              <p className="text-sm text-gray-400">Veterans (5+ years)</p>
              <p className="text-lg font-bold text-purple-400">
                {turnoverData.new_hire_metrics.veteran_employees_5_plus_years?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-white/5 p-4">
              <p className="text-sm text-gray-400">Long tenure (10+ years)</p>
              <p className="text-lg font-bold text-yellow-400">
                {turnoverData.new_hire_metrics.long_tenure_employees_10_plus_years?.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      )}

      {turnoverData?.turnover_by_department && (
        <div>
          <h4 className="text-lg font-semibold text-gray-300 mb-3">
            Turnover by Department
          </h4>
          <div className="space-y-3">
            {turnoverData.turnover_by_department.slice(0, 5).map((dept) => (
              <div key={dept.department} className="rounded-lg bg-white/5 p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-300">
                    {dept.department}
                  </span>
                  <span className="text-sm text-red-400 font-semibold">
                    {dept.turnover_rate}%
                  </span>
                </div>
                <div className="flex justify-between text-xs text-gray-500">
                  <span>{dept.terminations_last_year} terminations</span>
                  <span>{dept.total_employees} total employees</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
