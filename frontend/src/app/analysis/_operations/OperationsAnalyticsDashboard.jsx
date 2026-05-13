import DatasetInfo from "./components/DatasetInfo";
import OrderOverview from "./components/OrderOverview";
import InventoryManagement from "./components/InventoryManagement";
import SupplyChainPerformance from "./components/SupplyChainPerformance";
import QualityMetrics from "./components/QualityMetrics";
import ProductionEfficiency from "./components/ProductionEfficiency";
import DeliveryPerformance from "./components/DeliveryPerformance";
import RegionalOperations from "./components/RegionalOperations";
import OperationalCosts from "./components/OperationalCosts";
import OperationalTrends from "./components/OperationalTrends";

export default function OperationsAnalyticsDashboard({ analysis }) {
  return (
    <>
      {analysis && (
        <div>
          {/* Dataset Information */}
          {analysis.dataset_info && <DatasetInfo data={analysis} />}

          {/* Order Overview */}
          {analysis.order_overview && <OrderOverview data={analysis} />}

          {/* Inventory Management */}
          {(analysis.inventory_overview ||
            analysis.inventory_distribution ||
            analysis.product_inventory_alerts) && (
            <InventoryManagement data={analysis} />
          )}

          {/* Supply Chain Performance */}
          {(analysis.supplier_performance || analysis.lead_time_metrics) && (
            <SupplyChainPerformance data={analysis} />
          )}

          {/* Quality Metrics */}
          {analysis.quality_metrics && <QualityMetrics data={analysis} />}

          {/* Production Efficiency */}
          {analysis.production_efficiency && (
            <ProductionEfficiency data={analysis} />
          )}

          {/* Delivery Performance */}
          {analysis.delivery_performance && (
            <DeliveryPerformance data={analysis} />
          )}

          {/* Regional Operations */}
          {analysis.regional_operations && (
            <RegionalOperations data={analysis} />
          )}

          {/* Operational Costs */}
          {(analysis.cost_overview ||
            analysis.cost_by_product ||
            analysis.cost_by_supplier) && <OperationalCosts data={analysis} />}

          {/* Operational Trends */}
          {(analysis.monthly_operational_trends ||
            analysis.weekly_patterns ||
            analysis.seasonal_trends ||
            analysis.growth_metrics) && <OperationalTrends data={analysis} />}
        </div>
      )}
    </>
  );
}
