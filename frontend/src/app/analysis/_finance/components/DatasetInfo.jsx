import { Database, CheckCircle, AlertCircle, Calendar } from "lucide-react";

export default function DatasetInfo({ data }) {
  const datasetInfo = data.dataset_info;

  const getCompletenessColor = (percentage) => {
    if (percentage >= 90) return "text-green-400";
    if (percentage >= 70) return "text-yellow-400";
    return "text-red-400";
  };

  const getMappingColor = (percentage) => {
    if (percentage >= 80) return "text-green-400";
    if (percentage >= 60) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-white/20 bg-white/10 p-8 text-white shadow-2xl backdrop-blur-md transition-all duration-300 hover:scale-[1.02] hover:shadow-slate-500/20">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-slate-500/20 bg-slate-500/10">
          <Database className="h-6 w-6 text-slate-400" />
        </div>
        <div>
          <h3 className="text-2xl font-bold tracking-tight text-white">
            Dataset Information
          </h3>
          <p className="text-sm text-gray-400">
            Data quality and mapping insights
          </p>
        </div>
      </div>

      <hr className="my-2 border-gray-700" />

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-xl bg-white/5 p-4">
          <div className="flex items-center gap-3 mb-2">
            <Database className="h-5 w-5 text-slate-400" />
            <p className="text-sm text-gray-400">Dataset Size</p>
          </div>
          <p className="text-xl font-bold text-slate-400">
            {datasetInfo?.total_transactions?.toLocaleString()} rows
          </p>
          <p className="text-sm text-gray-500">
            {datasetInfo?.total_columns} columns
          </p>
        </div>

        <div className="rounded-xl bg-white/5 p-4">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle className="h-5 w-5 text-green-400" />
            <p className="text-sm text-gray-400">Data Completeness</p>
          </div>
          <p
            className={`text-xl font-bold ${getCompletenessColor(
              datasetInfo?.data_completeness
            )}`}
          >
            {datasetInfo?.data_completeness?.toFixed(1)}%
          </p>
          <p className="text-sm text-gray-500">Non-null values</p>
        </div>

        <div className="rounded-xl bg-white/5 p-4">
          <div className="flex items-center gap-3 mb-2">
            <AlertCircle className="h-5 w-5 text-amber-400" />
            <p className="text-sm text-gray-400">Column Mapping</p>
          </div>
          <p
            className={`text-xl font-bold ${getMappingColor(
              datasetInfo?.mapping_success_rate
            )}`}
          >
            {datasetInfo?.mapping_success_rate?.toFixed(1)}%
          </p>
          <p className="text-sm text-gray-500">
            {datasetInfo?.columns_mapped} mapped concepts
          </p>
        </div>

        {datasetInfo?.date_range && (
          <div className="rounded-xl bg-white/5 p-4">
            <div className="flex items-center gap-3 mb-2">
              <Calendar className="h-5 w-5 text-blue-400" />
              <p className="text-sm text-gray-400">Date Range</p>
            </div>
            <p className="text-lg font-bold text-blue-400">
              {datasetInfo.date_range.date_span_days} days
            </p>
            <p className="text-sm text-gray-500">
              {datasetInfo.date_range.start_date} to{" "}
              {datasetInfo.date_range.end_date}
            </p>
          </div>
        )}
      </div>

      {datasetInfo?.available_analyses && (
        <div>
          <h4 className="text-lg font-semibold text-gray-300 mb-3">
            Available Analyses
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {datasetInfo.available_analyses.map((analysis) => (
              <div
                key={analysis}
                className="rounded-lg bg-white/5 p-3 text-center"
              >
                <p className="text-sm font-medium text-slate-300 capitalize">
                  {analysis.replace(/_/g, " ")}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
