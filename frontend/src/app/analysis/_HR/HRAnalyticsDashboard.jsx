import AttendanceMetrics from "./components/AttendanceMetrics";
import CompensationOverview from "./components/CompensationOverview";
import DemographicsOverview from "./components/DemographicsOverview";
import DepartmentMetrics from "./components/DepartmentMetrics";
import HRDatasetInfo from "./components/HRDatasetInfo";
import PerformanceMetrics from "./components/PerformanceMetrics";
import TrainingMetrics from "./components/TrainingMetrics";
import TurnoverMetrics from "./components/TurnoverMetrics";
import WorkforceOverview from "./components/WorkforceOverview";

export default function HRAnalyticsDashboard({ analysis }) {
  return (
    <>
      {analysis && (
        <div>
          {/* HR Dataset Information */}
          {analysis.dataset_info && <HRDatasetInfo data={analysis} />}

          {/* Workforce Overview */}
          {analysis.workforce_overview && <WorkforceOverview data={analysis} />}

          {/* Compensation Overview */}
          {analysis.compensation_overview && (
            <CompensationOverview data={analysis} />
          )}

          {/* Department Metrics */}
          {analysis.department_metrics && <DepartmentMetrics data={analysis} />}

          {/* Performance Metrics */}
          {analysis.performance_overview && (
            <PerformanceMetrics data={analysis} />
          )}

          {/* Turnover & Retention */}
          {(analysis.tenure_metrics || analysis.turnover_metrics) && (
            <TurnoverMetrics data={analysis} />
          )}

          {/* Training & Development */}
          {analysis.training_overview && <TrainingMetrics data={analysis} />}

          {/* Demographics */}
          {analysis.demographics && <DemographicsOverview data={analysis} />}

          {/* Attendance & Leave */}
          {analysis.attendance_metrics && <AttendanceMetrics data={analysis} />}
        </div>
      )}
    </>
  );
}
