import {
  Package2,
  AlertTriangle,
  TrendingDown,
  TrendingUp,
} from "lucide-react";

export default function InventoryMetrics({ data }) {
  const inventory = data.inventory_metrics || {};
  const alerts = data.inventory_alerts || {};

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-amber-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-amber-600">
            <Package2 className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Inventory Metrics
          </span>
        </div>
        <span className="rounded-full bg-amber-600/20 px-4 py-1 text-sm font-medium text-amber-400">
          Stock
        </span>
      </div>

      {Object.keys(inventory).length > 0 && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Total Inventory</p>
              <p className="text-xl font-bold text-amber-400">
                ${inventory.total_inventory_value?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Avg Per Product</p>
              <p className="text-xl font-bold text-amber-400">
                ${inventory.avg_inventory_per_product?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Out of Stock</p>
              <p className="text-xl font-bold text-red-400">
                {inventory.out_of_stock}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Low Stock Alert</p>
              <p className="text-xl font-bold text-orange-400">
                {inventory.low_stock_products}
              </p>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />
        </>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Low Stock Items */}
        {alerts.low_stock_items && alerts.low_stock_items.length > 0 && (
          <div className="rounded-lg bg-red-900/20 border border-red-500/30 p-4">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="h-5 w-5 text-red-400" />
              <h3 className="text-lg font-semibold text-red-300">
                Low Stock Alert
              </h3>
            </div>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {alerts.low_stock_items.slice(0, 8).map((item, index) => (
                <div
                  key={item.product}
                  className="flex items-center justify-between bg-gray-800/50 rounded-lg p-3"
                >
                  <span className="text-white font-medium truncate mr-2">
                    {item.product}
                  </span>
                  <div className="flex items-center gap-2">
                    <TrendingDown className="h-4 w-4 text-red-400" />
                    <span className="text-red-400 font-bold">
                      {item.stock_level}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* High Stock Items */}
        {alerts.high_stock_items && alerts.high_stock_items.length > 0 && (
          <div className="rounded-lg bg-blue-900/20 border border-blue-500/30 p-4">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="h-5 w-5 text-blue-400" />
              <h3 className="text-lg font-semibold text-blue-300">
                High Stock Items
              </h3>
            </div>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {alerts.high_stock_items.slice(0, 8).map((item, index) => (
                <div
                  key={item.product}
                  className="flex items-center justify-between bg-gray-800/50 rounded-lg p-3"
                >
                  <span className="text-white font-medium truncate mr-2">
                    {item.product}
                  </span>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-blue-400" />
                    <span className="text-blue-400 font-bold">
                      {item.stock_level.toLocaleString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {Object.keys(inventory).length === 0 &&
        (!alerts.low_stock_items || alerts.low_stock_items.length === 0) &&
        (!alerts.high_stock_items || alerts.high_stock_items.length === 0) && (
          <div className="text-center py-8">
            <Package2 className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">No inventory data available</p>
          </div>
        )}
    </div>
  );
}
