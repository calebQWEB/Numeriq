import { Users2, Cake } from "lucide-react";
import { useState } from "react";

export default function DemographicsOverview({ data }) {
  const [activeTab, setActiveTab] = useState("age");
  const demographicsData = data.demographics;

  if (!demographicsData) return null;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-cyan-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-cyan-600">
            <Users2 className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Workforce Demographics
          </span>
        </div>
        <span className="rounded-full bg-cyan-600/20 px-4 py-1 text-sm font-medium text-cyan-400">
          Diversity
        </span>
      </div>

      {demographicsData?.age_metrics && (
        <div className="flex items-end justify-between">
          <span className="text-5xl font-extrabold text-cyan-400">
            {demographicsData.age_metrics.avg_age?.toFixed(1)}
          </span>
          <div className="flex items-center text-xl font-semibold text-gray-400">
            <Cake className="h-5 w-5 mr-2" />
            <span>Average Age</span>
          </div>
        </div>
      )}

      <hr className="my-4 border-gray-700" />

      {/* Tab Navigation */}
      <div className="flex gap-2">
        {demographicsData?.age_distribution && (
          <button
            onClick={() => setActiveTab("age")}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              activeTab === "age"
                ? "bg-cyan-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            Age Distribution
          </button>
        )}
        {demographicsData?.gender_distribution && (
          <button
            onClick={() => setActiveTab("gender")}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              activeTab === "gender"
                ? "bg-cyan-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            Gender Distribution
          </button>
        )}
      </div>

      {demographicsData?.age_metrics && (
        <div className="grid grid-cols-3 gap-4">
          <div className="rounded-lg bg-gray-800 p-4">
            <p className="text-sm text-gray-400">Median Age</p>
            <p className="text-xl font-bold text-cyan-400">
              {demographicsData.age_metrics.median_age?.toFixed(1)}
            </p>
          </div>
          <div className="rounded-lg bg-gray-800 p-4">
            <p className="text-sm text-gray-400">Youngest</p>
            <p className="text-xl font-bold text-cyan-400">
              {demographicsData.age_metrics.age_range?.min}
            </p>
          </div>
          <div className="rounded-lg bg-gray-800 p-4">
            <p className="text-sm text-gray-400">Oldest</p>
            <p className="text-xl font-bold text-cyan-400">
              {demographicsData.age_metrics.age_range?.max}
            </p>
          </div>
        </div>
      )}

      {/* Age Distribution Tab */}
      {activeTab === "age" && demographicsData?.age_distribution && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Age Groups
          </h3>
          <div className="space-y-4">
            {demographicsData.age_distribution?.map((ageGroup) => {
              const maxCount = Math.max(
                ...(demographicsData.age_distribution?.map(
                  (d) => d.employee_count
                ) || [1])
              );

              return (
                <div
                  key={ageGroup?.age_group}
                  className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
                >
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium text-gray-400 group-hover:text-gray-200">
                      {ageGroup?.age_group}
                    </span>
                    <span className="font-semibold text-white">
                      {ageGroup?.employee_count} employees
                    </span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
                    <div
                      className="h-full rounded-full bg-cyan-500 transition-all duration-500"
                      style={{
                        width: `${
                          (ageGroup?.employee_count / maxCount) * 100
                        }%`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Gender Distribution Tab */}
      {activeTab === "gender" && demographicsData?.gender_distribution && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Gender Breakdown
          </h3>
          <div className="grid grid-cols-2 gap-4">
            {demographicsData.gender_distribution?.map((gender) => (
              <div
                key={gender?.gender}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700 text-center"
              >
                <p className="text-sm text-gray-400">{gender?.gender}</p>
                <p className="text-2xl font-bold text-cyan-400">
                  {gender?.employee_count}
                </p>
                <p className="text-lg text-cyan-300">{gender?.percentage}%</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
