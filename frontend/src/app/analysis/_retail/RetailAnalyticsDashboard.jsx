import ProductPerformance from "./components/ProductPerformance";
import CategoryPerformance from "./components/CategoryPerformance";
import BrandPerformance from "./components/BrandPerformance";
import InventoryMetrics from "./components/InventoryMetrics";
import PricingAnalysis from "./components/PricingAnalysis";
import StorePerformance from "./components/StorePerformance";
import SeasonalTrends from "./components/SeasonalTrends";
import DatasetInfo from "./components/DatasetInfo";

export default function RetailAnalyticsDashboard({ analysis }) {
  return (
    <>
      {analysis && (
        <div>
          {/* Dataset Information */}
          {analysis.dataset_info && <DatasetInfo data={analysis} />}

          {/* Product Performance */}
          {(analysis.top_performing_products ||
            analysis.top_selling_products) && (
            <ProductPerformance data={analysis} />
          )}

          {/* Category Performance */}
          {analysis.category_performance && (
            <CategoryPerformance data={analysis} />
          )}

          {/* Brand Performance */}
          {analysis.brand_performance && <BrandPerformance data={analysis} />}

          {/* Inventory Metrics */}
          {(analysis.inventory_metrics || analysis.inventory_alerts) && (
            <InventoryMetrics data={analysis} />
          )}

          {/* Pricing Analysis */}
          {(analysis.pricing_metrics ||
            analysis.margin_analysis ||
            analysis.discount_analysis) && <PricingAnalysis data={analysis} />}

          {/* Store Performance */}
          {analysis.store_performance && <StorePerformance data={analysis} />}

          {/* Seasonal & Time Trends */}
          {(analysis.seasonal_trends || analysis.daily_patterns) && (
            <SeasonalTrends data={analysis} />
          )}
        </div>
      )}
    </>
  );
}
