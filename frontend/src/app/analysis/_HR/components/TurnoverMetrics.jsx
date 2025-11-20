import { UserMinus, Clock, TrendingUp } from "lucide-react";

export default function TurnoverMetrics({ data }) {
  const tenureData = data.tenure_metrics;
  const turnoverData = data.turnover_metrics;
  const hiringData = data.hiring_trends;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-red-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-600">
            <UserMinus className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Turnover & Retention
          </span>
        </div>
        <span className="rounded-full bg-red-600/20 px-4 py-1 text-sm font-medium text-red-400">
          Metrics
        </span>
      </div>

      {turnoverData && (
        <div className="flex items-end justify-between">
          <span className="text-5xl font-extrabold text-red-400">
            {turnoverData?.annual_turnover_rate}%
          </span>
          <div className="flex items-center text-xl font-semibold text-gray-400">
            <span className="mr-1">Annual Turnover</span>
          </div>
        </div>
      )}

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-2 gap-4">
        {tenureData && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="h-4 w-4 text-blue-400" />
                <p className="text-sm text-gray-400">Average Tenure</p>
              </div>
              <p className="text-xl font-bold text-blue-400">
                {tenureData?.avg_tenure_years?.toFixed(1)} years
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Long-term Employees</p>
              <p className="text-xl font-bold text-green-400">
                {tenureData?.long_tenure_employees} (5+ years)
              </p>
            </div>
          </>
        )}

        {turnoverData && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Terminations (Last Year)</p>
              <p className="text-xl font-bold text-red-400">
                {turnoverData?.terminations_last_year}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Terminations</p>
              <p className="text-xl font-bold text-red-400">
                {turnoverData?.total_terminations}
              </p>
            </div>
          </>
        )}

        {tenureData?.new_hires_last_year && (
          <div className="rounded-lg bg-gray-800 p-4 col-span-2">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="h-4 w-4 text-green-400" />
              <p className="text-sm text-gray-400">New Hires (Last Year)</p>
            </div>
            <p className="text-xl font-bold text-green-400">
              {tenureData?.new_hires_last_year}
            </p>
          </div>
        )}
      </div>

      {hiringData && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Recent Hiring Trends
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {hiringData?.slice(-6).map((trend) => (
              <div
                key={trend?.month}
                className="rounded-lg bg-gray-800 p-3 text-center"
              >
                <p className="text-xs text-gray-400">{trend?.month}</p>
                <p className="text-lg font-bold text-blue-400">
                  {trend?.hires} hires
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
