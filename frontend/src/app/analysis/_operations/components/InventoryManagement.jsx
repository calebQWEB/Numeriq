import { Warehouse } from "lucide-react";

export default function InventoryManagement({ data }) {
  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-purple-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-purple-600">
            <Warehouse className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Inventory Management
          </span>
        </div>
        <span className="rounded-full bg-purple-600/20 px-4 py-1 text-sm font-medium text-purple-400">
          Stock Control
        </span>
      </div>

      {data.inventory_overview && (
        <>
          <div className="flex items-end justify-between">
            <span className="text-5xl font-extrabold text-purple-400">
              {data.inventory_overview?.total_inventory_units?.toLocaleString()}
            </span>
            <div className="flex items-center text-xl font-semibold text-gray-400">
              <span className="mr-1">Units</span>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />

          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Average per Item</p>
              <p className="text-xl font-bold text-purple-400">
                {data.inventory_overview?.average_inventory_per_item?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Inventory Items</p>
              <p className="text-xl font-bold text-purple-400">
                {data.inventory_overview?.inventory_items?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Zero Stock Items</p>
              <p className="text-xl font-bold text-red-400">
                {data.inventory_overview?.zero_inventory_items?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Low Stock Items</p>
              <p className="text-xl font-bold text-orange-400">
                {data.inventory_overview?.low_inventory_items?.toLocaleString()}
              </p>
            </div>
          </div>
        </>
      )}

      {data.inventory_distribution && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Inventory Distribution
          </h3>
          <ul className="mt-4 space-y-4">
            {data.inventory_distribution?.map((dist) => (
              <li
                key={dist?.level}
                className="group flex flex-col gap-2 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {dist?.level} Stock
                  </span>
                  <span className="font-semibold text-white">
                    {dist.item_count?.toLocaleString()} items
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.reorder_analysis && (
        <div className="rounded-lg bg-red-900/20 border border-red-500/30 p-4">
          <h3 className="text-lg font-semibold text-red-400 mb-3">
            Reorder Alerts
          </h3>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-400">
              Items Below Reorder Point
            </span>
            <span className="text-lg font-bold text-red-400">
              {data.reorder_analysis?.items_below_reorder_point?.toLocaleString()}
            </span>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm text-gray-400">Percentage Below</span>
            <span className="text-sm font-medium text-red-400">
              {data.reorder_analysis?.percentage_below_reorder}%
            </span>
          </div>
        </div>
      )}

      {data.product_inventory_alerts?.lowest_stock_products && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Lowest Stock Products
          </h3>
          <ul className="mt-4 space-y-4">
            {data.product_inventory_alerts.lowest_stock_products
              ?.slice(0, 5)
              .map((product) => (
                <li
                  key={product?.product}
                  className="group flex items-center justify-between rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
                >
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {product?.product}
                  </span>
                  <span className="font-semibold text-orange-400">
                    {product.total_inventory?.toLocaleString()} units
                  </span>
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
}
