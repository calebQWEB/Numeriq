import { Store, MapPin, Users, ShoppingBag } from "lucide-react";

export default function StorePerformance({ data }) {
  const stores = data.store_performance || [];
  const maxRevenue = Math.max(
    ...stores.map((store) => store.total_revenue || 0)
  );
  const totalRevenue = stores.reduce(
    (sum, store) => sum + (store.total_revenue || 0),
    0
  );

  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-teal-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-teal-600">
            <Store className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Store Performance
          </span>
        </div>
        <span className="rounded-full bg-teal-600/20 px-4 py-1 text-sm font-medium text-teal-400">
          Locations
        </span>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-gray-300">
          <MapPin className="h-5 w-5" />
          <span className="text-lg font-medium">
            {stores.length} Store Locations
          </span>
        </div>
        <div className="flex items-center gap-2 text-gray-300">
          <ShoppingBag className="h-5 w-5" />
          <span className="text-lg font-medium">
            ${totalRevenue.toLocaleString()} Total Revenue
          </span>
        </div>
      </div>

      <hr className="my-4 border-gray-700" />

      {stores.length > 0 && (
        <div className="space-y-4">
          {stores.map((store, index) => (
            <div
              key={store.store}
              className="group flex flex-col gap-4 rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-teal-600/20 text-sm font-bold text-teal-400">
                    {index + 1}
                  </div>
                  <div className="flex flex-col">
                    <span className="font-semibold text-white group-hover:text-teal-300 transition-colors">
                      {store.store}
                    </span>
                    <span className="text-sm text-gray-400">
                      Store Location
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-400">
                    ${store.total_revenue?.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-400">
                    {((store.total_revenue / totalRevenue) * 100).toFixed(1)}%
                    of total
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="text-center rounded-lg bg-gray-900/50 p-3">
                  <div className="flex items-center justify-center gap-1 text-gray-400 mb-1">
                    <Users className="h-4 w-4" />
                    <span className="text-xs">Transactions</span>
                  </div>
                  <div className="text-lg font-bold text-blue-400">
                    {store.total_transactions?.toLocaleString()}
                  </div>
                </div>
                <div className="text-center rounded-lg bg-gray-900/50 p-3">
                  <div className="text-gray-400 text-xs mb-1">
                    Avg Transaction
                  </div>
                  <div className="text-lg font-bold text-purple-400">
                    ${store.avg_transaction_value?.toFixed(2)}
                  </div>
                </div>
                <div className="text-center rounded-lg bg-gray-900/50 p-3">
                  <div className="text-gray-400 text-xs mb-1">Units Sold</div>
                  <div className="text-lg font-bold text-orange-400">
                    {store.units_sold?.toLocaleString()}
                  </div>
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Revenue Performance</span>
                  <span>
                    {((store.total_revenue / maxRevenue) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="h-3 w-full overflow-hidden rounded-full bg-gray-700">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-teal-500 to-cyan-500 transition-all duration-500"
                    style={{
                      width: `${(store.total_revenue / maxRevenue) * 100}%`,
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {stores.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="rounded-lg bg-gray-800 p-4 text-center">
            <div className="text-sm text-gray-400 mb-1">Best Performer</div>
            <div className="text-lg font-bold text-teal-400">
              {stores[0]?.store}
            </div>
          </div>
          <div className="rounded-lg bg-gray-800 p-4 text-center">
            <div className="text-sm text-gray-400 mb-1">Highest AOV</div>
            <div className="text-lg font-bold text-purple-400">
              $
              {Math.max(
                ...stores.map((s) => s.avg_transaction_value || 0)
              ).toFixed(2)}
            </div>
          </div>
          <div className="rounded-lg bg-gray-800 p-4 text-center">
            <div className="text-sm text-gray-400 mb-1">Most Transactions</div>
            <div className="text-lg font-bold text-blue-400">
              {Math.max(
                ...stores.map((s) => s.total_transactions || 0)
              ).toLocaleString()}
            </div>
          </div>
          <div className="rounded-lg bg-gray-800 p-4 text-center">
            <div className="text-sm text-gray-400 mb-1">Total Units</div>
            <div className="text-lg font-bold text-orange-400">
              {stores
                .reduce((sum, store) => sum + (store.units_sold || 0), 0)
                .toLocaleString()}
            </div>
          </div>
        </div>
      )}

      {stores.length === 0 && (
        <div className="text-center py-8">
          <Store className="h-16 w-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">No store performance data available</p>
        </div>
      )}
    </div>
  );
}
