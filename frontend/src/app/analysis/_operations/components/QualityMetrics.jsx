import { Shield } from "lucide-react";

export default function QualityMetrics({ data }) {
  const qualityData = data.quality_metrics;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-emerald-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-600">
            <Shield className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Quality Metrics
          </span>
        </div>
        <span className="rounded-full bg-emerald-600/20 px-4 py-1 text-sm font-medium text-emerald-400">
          Quality Control
        </span>
      </div>

      {qualityData?.defect_analysis && (
        <>
          <div className="flex items-end justify-between">
            <span className="text-5xl font-extrabold text-emerald-400">
              {(qualityData.defect_analysis.avg_defect_rate * 100)?.toFixed(2)}%
            </span>
            <div className="flex items-center text-xl font-semibold text-gray-400">
              <span className="mr-1">Avg Defect Rate</span>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />
        </>
      )}

      <div className="grid grid-cols-2 gap-4">
        {qualityData?.defect_analysis && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Defects</p>
              <p className="text-xl font-bold text-red-400">
                {qualityData.defect_analysis?.total_defects?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Zero Defect Items</p>
              <p className="text-xl font-bold text-emerald-400">
                {qualityData.defect_analysis?.zero_defect_items?.toLocaleString()}
              </p>
            </div>
          </>
        )}

        {qualityData?.quality_score_analysis && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Avg Quality Score</p>
              <p className="text-xl font-bold text-emerald-400">
                {qualityData.quality_score_analysis?.avg_quality_score?.toFixed(
                  1
                )}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">High Quality Items</p>
              <p className="text-xl font-bold text-emerald-400">
                {qualityData.quality_score_analysis?.high_quality_items?.toLocaleString()}
              </p>
            </div>
          </>
        )}

        {qualityData?.error_analysis && (
          <>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Avg Error Rate</p>
              <p className="text-xl font-bold text-yellow-400">
                {(qualityData.error_analysis.avg_error_rate * 100)?.toFixed(2)}%
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Error Free Items</p>
              <p className="text-xl font-bold text-emerald-400">
                {qualityData.error_analysis?.error_free_items?.toLocaleString()}
              </p>
            </div>
          </>
        )}
      </div>

      {qualityData?.quality_score_analysis && (
        <div className="rounded-lg bg-gray-800 p-4">
          <h3 className="text-lg font-semibold text-gray-300 mb-3">
            Quality Distribution
          </h3>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-400">High Quality Items</span>
            <span className="text-sm font-bold text-emerald-400">
              {qualityData.quality_score_analysis?.high_quality_items?.toLocaleString()}
            </span>
          </div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-400">Low Quality Items</span>
            <span className="text-sm font-bold text-red-400">
              {qualityData.quality_score_analysis?.low_quality_items?.toLocaleString()}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-400">Quality Std Deviation</span>
            <span className="text-sm font-medium text-white">
              {qualityData.quality_score_analysis?.quality_std_dev?.toFixed(2)}
            </span>
          </div>
        </div>
      )}

      {qualityData?.product_quality_issues && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Products with Quality Issues
          </h3>
          <ul className="mt-4 space-y-4">
            {qualityData.product_quality_issues?.slice(0, 5).map((product) => (
              <li
                key={product?.product}
                className="group flex items-center justify-between rounded-lg bg-red-900/20 border border-red-500/30 p-4 transition-colors duration-200 hover:bg-red-800/30"
              >
                <span className="font-medium text-gray-400 group-hover:text-gray-200">
                  {product?.product}
                </span>
                <span className="font-semibold text-red-400">
                  {(product.avg_defect_rate * 100)?.toFixed(2)}% defects
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
