"use client";
import { useAuth } from "@/provider/AuthProvider";
import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import RetailAnalyticsDashboard from "../_retail/RetailAnalyticsDashboard";
import SalesAnalyticsDashboard from "../_sales/SalesAnalyticsDashboard";
import FinanceAnalyticsDashboard from "../_finance/FinanceAnalyticsDashboard";
import HRAnalyticsDashboard from "../_HR/HRAnalyticsDashboard";
import RetailAIAnalysis from "../_retail/RetailAIAnalysis";
import HRAIAnalytics from "../_HR/HRAIAnalytics";
import SalesAIAnalytics from "../_sales/SalesAIAnalytics";
import FinanceAIAnalytics from "../_finance/FinanceAIAnalytics";
import OperationsAIAnalytics from "../_operations/OperationsAIAnalytics";
import OperationsAnalyticsDashboard from "../_operations/OperationsAnalyticsDashboard";
import ExportButton from "../../../components/ExportButton";
import LoadingSpinner from "@/utils/LoadingSpinner";
import { fetchFileById, getSubscription, viewAnalysis } from "@/lib/api";

const page = () => {
  const { user, session } = useAuth();
  const { fileId } = useParams();
  const [fileData, setFileData] = useState(null);
  const [getFileError, setGetFileError] = useState("");
  const [getFileLoading, setGetFileLoading] = useState(false);
  const [fileAnalytics, setFileAnalytics] = useState(null);
  const [getAnalyticsError, setGetAnalyticsError] = useState("");
  const [getAnalyticsLoading, setGetAnalyticsLoading] = useState(false);
  const [currentAnalysisMethod, setCurrentAnaylysisMethod] =
    useState("Manual Analysis");

  const [subscription, setSubscription] = useState(null);
  const [subscriptionError, setSubscriptionError] = useState(null);
  const [subscriptionLoading, setSubscriptionLoading] = useState(false);

  const viewAnalytics = async () => {
    setGetAnalyticsLoading(true);
    setGetAnalyticsError("");
    try {
      const result = await viewAnalysis(fileId, session);
      setFileAnalytics(result);
      console.log("File analysis result:", result);
    } catch (error) {
      console.log("Error viewing analytics:", error);
      setGetAnalyticsError(error.message || "Failed to view analytics");
    } finally {
      setGetAnalyticsLoading(false);
    }
  };

  const fetchFileData = async () => {
    setGetFileLoading(true);
    setGetFileError("");
    try {
      const response = await fetchFileById(fileId, session);
      setFileData(response);
      console.log("File data:", response);
    } catch (error) {
      console.log("Error fetching file data:", error);
      setGetFileError(
        error.message || "An error occurred while fetching file data"
      );
    } finally {
      setGetFileLoading(false);
    }
  };

  const subscriptionStatus = async () => {
    setSubscriptionLoading(true);
    setSubscriptionError(null);

    try {
      const data = await getSubscription(session);
      setSubscription(data);
    } catch (error) {
      setSubscriptionError(error.message);
    } finally {
      setSubscriptionLoading(false);
    }
  };

  const showAnalytics = (spreadsheet_type, analysis) => {
    switch (spreadsheet_type) {
      case "Retail":
        return (
          <RetailAnalyticsDashboard
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "HR":
        return (
          <HRAnalyticsDashboard
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "Sales":
        return (
          <SalesAnalyticsDashboard
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "Finance":
        return (
          <FinanceAnalyticsDashboard
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "Operations":
        return (
          <OperationsAnalyticsDashboard
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      default:
        return <div>No analytics available for this spreadsheet type.</div>;
    }
  };

  const showAIAnalytics = (analysis, spreadsheet_type) => {
    switch (spreadsheet_type) {
      case "Retail":
        return (
          <RetailAIAnalysis
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "HR":
        return (
          <HRAIAnalytics
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "Sales":
        return (
          <SalesAIAnalytics
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "Finance":
        return (
          <FinanceAIAnalytics
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      case "Operations":
        return (
          <OperationsAIAnalytics
            analysis={analysis}
            spreadsheet_type={spreadsheet_type}
          />
        );
      default:
        return <div>No analytics available for this spreadsheet type.</div>;
    }
  };
  useEffect(() => {
    if (fileId && session) {
      viewAnalytics();
      fetchFileData();
      subscriptionStatus();
    }
  }, [fileId, session]);

  if (getFileLoading || getAnalyticsLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner message="Please wait...." />
      </div>
    );
  }

  const isActive =
    subscription?.status === "active" && subscription?.plan !== "free";

  return (
    <section className="px-8 py-4 bg-gray-900 min-h-screen mt-10">
      {/* File Metadata */}
      <div className="flex items-center justify-between mb-8">
        <div className="grid gap-4">
          {fileData ? (
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-2xl font-extrabold leading-tight tracking-tight text-gray-400">
                Analytics for {fileData.filename}
              </h1>
            </div>
          ) : (
            <p className="text-gray-400">
              No analytics data available for this file.
            </p>
          )}

          {fileAnalytics && (
            <div className="mb-6 flex items-center gap-4">
              {["Manual Analysis", "AI Analysis"].map((method) => (
                <button
                  key={method}
                  onClick={() => {
                    setCurrentAnaylysisMethod(method);
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                >
                  {method}
                </button>
              ))}
            </div>
          )}
        </div>

        <ExportButton fileId={fileId} session={session} isActive={isActive} />
      </div>

      {fileAnalytics && (
        <>
          {currentAnalysisMethod === "Manual Analysis" &&
            showAnalytics(
              fileData?.spreadsheet_type,
              fileAnalytics?.computed_insights?.Sheet1
            )}

          {currentAnalysisMethod === "AI Analysis" &&
            showAIAnalytics(
              fileAnalytics?.ai_insights,
              fileData?.spreadsheet_type
            )}
        </>
      )}
    </section>
  );
};

export default page;
