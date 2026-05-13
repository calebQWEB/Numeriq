import { BookOpen, Award } from "lucide-react";

export default function TrainingMetrics({ data }) {
  const trainingData = data.training_overview;
  const trainingByDept = data.training_by_department;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-indigo-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-600">
            <BookOpen className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Training & Development
          </span>
        </div>
        <span className="rounded-full bg-indigo-600/20 px-4 py-1 text-sm font-medium text-indigo-400">
          Learning
        </span>
      </div>

      <div className="flex items-end justify-between">
        <span className="text-5xl font-extrabold text-indigo-400">
          {trainingData?.total_training_hours?.toLocaleString()}
        </span>
        <div className="flex items-center text-xl font-semibold text-gray-400">
          <span className="mr-1">Total Hours</span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Average Hours</p>
          <p className="text-xl font-bold text-indigo-400">
            {trainingData?.avg_training_hours?.toFixed(1)}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4">
          <p className="text-sm text-gray-400">Per Employee</p>
          <p className="text-xl font-bold text-indigo-400">
            {trainingData?.avg_training_per_employee?.toFixed(1)}
          </p>
        </div>
        <div className="rounded-lg bg-gray-800 p-4 flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-400">Employees Trained</p>
            <p className="text-xl font-bold text-green-400">
              {trainingData?.employees_with_training}
            </p>
          </div>
          <Award className="h-6 w-6 text-green-400" />
        </div>
      </div>

      {trainingByDept && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300 mb-4">
            Training by Department
          </h3>
          <div className="space-y-4">
            {trainingByDept?.map((dept) => (
              <div
                key={dept?.department}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-300 group-hover:text-white">
                    {dept?.department}
                  </span>
                  <span className="text-sm text-gray-400">
                    {dept?.employees_trained} trained
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Average Hours</p>
                    <p className="text-lg font-bold text-indigo-400">
                      {dept?.avg_training_hours?.toFixed(1)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Total Hours</p>
                    <p className="text-lg font-bold text-indigo-400">
                      {dept?.total_training_hours?.toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700 mt-2">
                  <div
                    className="h-full rounded-full bg-indigo-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(
                        (dept?.total_training_hours /
                          (trainingData?.total_training_hours || 1)) *
                          100,
                        100
                      )}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
