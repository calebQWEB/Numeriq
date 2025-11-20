import { Calendar, Stethoscope, Plane, Clock } from "lucide-react";
import { useState } from "react";

export default function AttendanceMetrics({ data }) {
  const [activeTab, setActiveTab] = useState("sick");
  const attendanceData = data.attendance_metrics;

  if (!attendanceData) return null;

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-teal-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-teal-600">
            <Calendar className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Attendance & Leave
          </span>
        </div>
        <span className="rounded-full bg-teal-600/20 px-4 py-1 text-sm font-medium text-teal-400">
          Time Off
        </span>
      </div>

      <hr className="my-4 border-gray-700" />

      {/* Tab Navigation */}
      <div className="flex gap-2">
        {attendanceData?.sick_leave && (
          <button
            onClick={() => setActiveTab("sick")}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              activeTab === "sick"
                ? "bg-teal-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            Sick Leave
          </button>
        )}
        {attendanceData?.vacation && (
          <button
            onClick={() => setActiveTab("vacation")}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              activeTab === "vacation"
                ? "bg-teal-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            Vacation
          </button>
        )}
        {attendanceData?.overtime && (
          <button
            onClick={() => setActiveTab("overtime")}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              activeTab === "overtime"
                ? "bg-teal-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            Overtime
          </button>
        )}
      </div>

      {/* Sick Leave Tab */}
      {activeTab === "sick" && attendanceData?.sick_leave && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Stethoscope className="h-5 w-5 text-red-400" />
            <h3 className="text-xl font-semibold text-gray-300">
              Sick Leave Analysis
            </h3>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Sick Days</p>
              <p className="text-3xl font-bold text-red-400">
                {attendanceData.sick_leave.total_sick_days?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Employees Used Sick Leave</p>
              <p className="text-3xl font-bold text-red-400">
                {attendanceData.sick_leave.employees_with_sick_leave}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Average per Employee</p>
              <p className="text-xl font-bold text-red-400">
                {attendanceData.sick_leave.avg_sick_days?.toFixed(1)} days
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Median Sick Days</p>
              <p className="text-xl font-bold text-red-400">
                {attendanceData.sick_leave.median_sick_days?.toFixed(1)} days
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Vacation Tab */}
      {activeTab === "vacation" && attendanceData?.vacation && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Plane className="h-5 w-5 text-blue-400" />
            <h3 className="text-xl font-semibold text-gray-300">
              Vacation Usage
            </h3>
          </div>

          <div className="grid grid-cols-1 gap-4 mb-6">
            <div className="rounded-lg bg-gray-800 p-4 text-center">
              <p className="text-sm text-gray-400">Total Vacation Days</p>
              <p className="text-4xl font-bold text-blue-400">
                {attendanceData.vacation.total_vacation_days?.toLocaleString()}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Average per Employee</p>
              <p className="text-xl font-bold text-blue-400">
                {attendanceData.vacation.avg_vacation_days?.toFixed(1)} days
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Median Vacation Days</p>
              <p className="text-xl font-bold text-blue-400">
                {attendanceData.vacation.median_vacation_days?.toFixed(1)} days
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Overtime Tab */}
      {activeTab === "overtime" && attendanceData?.overtime && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Clock className="h-5 w-5 text-amber-400" />
            <h3 className="text-xl font-semibold text-gray-300">
              Overtime Analysis
            </h3>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Overtime Hours</p>
              <p className="text-3xl font-bold text-amber-400">
                {attendanceData.overtime.total_overtime_hours?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Employees with Overtime</p>
              <p className="text-3xl font-bold text-amber-400">
                {attendanceData.overtime.employees_with_overtime}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">
                Average Overtime per Employee
              </p>
              <p className="text-xl font-bold text-amber-400">
                {attendanceData.overtime.avg_overtime_hours?.toFixed(1)} hours
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
