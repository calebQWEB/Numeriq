import { DollarSign } from "lucide-react";

export default function CompensationOverview({ data }) {
  const compensationData = data.compensation_overview;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-green-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-600">
            <DollarSign className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Compensation Overview
          </span>
        </div>
        <span className="rounded-full bg-green-600/20 px-4 py-1 text-sm font-medium text-green-400">
          Salaries
        </span>
      </div>

      <div className="flex items-end justify-between">
        <span className="text-5xl font-extrabold text-green-400">
          ${compensationData?.total_payroll?.toLocaleString()}
        </span>
        <div className="flex items-center text-xl font-semibold text-gray-400">
          <span className="mr-1">Total Payroll</span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Average Salary</p>
          <p className="text-xl font-bold text-green-400">
            ${compensationData?.avg_salary?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Median Salary</p>
          <p className="text-xl font-bold text-green-400">
            ${compensationData?.median_salary?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Salary Range</p>
          <p className="text-xl font-bold text-green-400">
            ${compensationData?.salary_range?.min?.toLocaleString()} - $
            {compensationData?.salary_range?.max?.toLocaleString()}
          </p>
        </div>
      </div>

      {data.salary_by_position && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Top Paying Positions
          </h3>
          <ul className="mt-4 space-y-4">
            {data.salary_by_position?.slice(0, 5).map((position) => (
              <li
                key={position?.position}
                className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {position?.position} ({position?.employee_count} employees)
                  </span>
                  <span className="font-semibold text-white">
                    ${position?.avg_salary?.toLocaleString()}
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-green-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(
                        (position?.avg_salary /
                          (compensationData?.salary_range?.max || 1)) *
                          100,
                        100
                      )}%`,
                    }}
                  />
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
