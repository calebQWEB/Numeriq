import {
  Database,
  CheckCircle,
  AlertCircle,
  Building,
  MapPin,
  Briefcase,
} from "lucide-react";

export default function HRDatasetInfo({ data }) {
  const datasetInfo = data.dataset_info;
  const diversityMetrics = data.diversity_metrics;

  const getCompletenessColor = (percentage) => {
    if (percentage >= 90) return "text-green-400";
    if (percentage >= 70) return "text-yellow-400";
    return "text-red-400";
  };

  const getMappingColor = (columnsTotal) => {
    const percentage = (datasetInfo?.columns_mapped / columnsTotal) * 100;
    if (percentage >= 70) return "text-green-400";
    if (percentage >= 50) return "text-yellow-400";
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
            HR Dataset Information
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
            {datasetInfo?.total_records?.toLocaleString()} records
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
              datasetInfo?.total_columns
            )}`}
          >
            {datasetInfo?.columns_mapped} mapped
          </p>
          <p className="text-sm text-gray-500">
            of {datasetInfo?.total_columns} columns
          </p>
        </div>

        {diversityMetrics && (
          <div className="rounded-xl bg-white/5 p-4">
            <div className="flex items-center gap-3 mb-2">
              <Building className="h-5 w-5 text-blue-400" />
              <p className="text-sm text-gray-400">Organizational Diversity</p>
            </div>
            <div className="space-y-1">
              {diversityMetrics?.unique_departments && (
                <p className="text-sm text-blue-400">
                  {diversityMetrics.unique_departments} departments
                </p>
              )}
              {diversityMetrics?.unique_positions && (
                <p className="text-sm text-blue-400">
                  {diversityMetrics.unique_positions} positions
                </p>
              )}
              {diversityMetrics?.unique_locations && (
                <p className="text-sm text-blue-400">
                  {diversityMetrics.unique_locations} locations
                </p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Available Analyses */}
      <div>
        <h4 className="text-lg font-semibold text-gray-300 mb-3">
          Available HR Analyses
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {data.workforce_overview && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">
                Workforce Overview
              </p>
            </div>
          )}
          {data.compensation_overview && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">
                Compensation Analysis
              </p>
            </div>
          )}
          {data.department_metrics && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">
                Department Metrics
              </p>
            </div>
          )}
          {data.performance_overview && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">
                Performance Analysis
              </p>
            </div>
          )}
          {(data.tenure_metrics || data.turnover_metrics) && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">
                Turnover & Retention
              </p>
            </div>
          )}
          {data.training_overview && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">
                Training & Development
              </p>
            </div>
          )}
          {data.demographics && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">Demographics</p>
            </div>
          )}
          {data.attendance_metrics && (
            <div className="rounded-lg bg-white/5 p-3 text-center">
              <p className="text-sm font-medium text-slate-300">
                Attendance & Leave
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
