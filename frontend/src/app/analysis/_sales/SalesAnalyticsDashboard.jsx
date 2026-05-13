"use client";
import React from "react";
import Revenue from "./components/Revenue";
import Customers from "./components/Customers";
import Products from "./components/Products";
import Region from "./components/Region";
import SalesPerformance from "./components/SalesPerformance";

const SalesAnalyticsDashboard = ({ analysis }) => {
  return (
    <>
      {analysis && (
        <div>
          {(analysis.total_revenue || analysis.sales_metrics) && (
            <Revenue data={analysis} />
          )}
          {analysis.top_customers && (
            <Customers
              data={analysis?.top_customers}
              metric={analysis?.customer_metrics}
            />
          )}
          {analysis.top_products && <Products data={analysis?.top_products} />}
          {analysis.regional_performance && (
            <Region data={analysis?.regional_performance} />
          )}
          {analysis.top_sales_reps && (
            <SalesPerformance data={analysis?.top_sales_reps} />
          )}
        </div>
      )}
    </>
  );
};

export default SalesAnalyticsDashboard;
