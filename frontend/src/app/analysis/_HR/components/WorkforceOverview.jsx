import { Users } from "lucide-react";

export default function WorkforceOverview({ data }) {
  const workforceData = data.workforce_overview;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-blue-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-600">
            <Users className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Workforce Overview
          </span>
        </div>
        <span className="rounded-full bg-blue-600/20 px-4 py-1 text-sm font-medium text-blue-400">
          Overview
        </span>
      </div>

      <div className="flex items-end justify-between">
        <span className="text-5xl font-extrabold text-blue-400">
          {workforceData?.total_employees?.toLocaleString()}
        </span>
        <div className="flex items-center text-xl font-semibold text-gray-400">
          <span className="mr-1">Total Employees</span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Active Employees</p>
          <p className="text-xl font-bold text-green-400">
            {workforceData?.active_employees?.toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Activity Rate</p>
          <p className="text-xl font-bold text-green-400">
            {workforceData?.total_employees > 0
              ? (
                  (workforceData?.active_employees /
                    workforceData?.total_employees) *
                  100
                ).toFixed(1)
              : 0}
            %
          </p>
        </div>
      </div>

      {data.department_distribution && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Department Distribution
          </h3>
          <ul className="mt-4 space-y-4">
            {data.department_distribution?.slice(0, 5).map((dept) => (
              <li
                key={dept?.department}
                className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {dept?.department}
                  </span>
                  <span className="font-semibold text-white">
                    {dept?.employee_count} ({dept?.percentage}%)
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-blue-500 transition-all duration-500"
                    style={{
                      width: `${dept?.percentage}%`,
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
