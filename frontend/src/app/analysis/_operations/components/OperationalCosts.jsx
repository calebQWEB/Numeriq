import { DollarSign } from "lucide-react";

export default function OperationalCosts({ data }) {
  return (
    <div className="mt-10 flex flex-col gap-6 bg-white/10 backdrop-blur-md border rounded-3xl border-white/20 p-8 text-white shadow-2xl transition-all duration-300 hover:scale-[1.02] hover:shadow-green-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-600">
            <DollarSign className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">
            Operational Costs
          </span>
        </div>
        <span className="rounded-full bg-green-600/20 px-4 py-1 text-sm font-medium text-green-400">
          Financial
        </span>
      </div>

      {data.cost_overview && (
        <>
          <div className="flex items-end justify-between">
            <span className="text-5xl font-extrabold text-green-400">
              ${data.cost_overview?.total_operational_costs?.toLocaleString()}
            </span>
            <div className="flex items-center text-xl font-semibold text-gray-400">
              <span className="mr-1">USD</span>
            </div>
          </div>

          <hr className="my-4 border-gray-700" />

          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Average Cost</p>
              <p className="text-xl font-bold text-green-400">
                ${data.cost_overview?.average_cost?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Median Cost</p>
              <p className="text-xl font-bold text-green-400">
                ${data.cost_overview?.median_cost?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Highest Cost</p>
              <p className="text-xl font-bold text-red-400">
                ${data.cost_overview?.highest_cost?.toLocaleString()}
              </p>
            </div>
            <div className="rounded-lg bg-gray-800 p-4">
              <p className="text-sm text-gray-400">Lowest Cost</p>
              <p className="text-xl font-bold text-blue-400">
                ${data.cost_overview?.lowest_cost?.toLocaleString()}
              </p>
            </div>
          </div>
        </>
      )}

      {data.cost_by_product && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Cost by Product
          </h3>
          <ul className="mt-4 space-y-4">
            {data.cost_by_product?.slice(0, 5).map((product) => (
              <li
                key={product?.product}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {product?.product}
                  </span>
                  <span className="font-semibold text-green-400">
                    ${product.total_cost?.toLocaleString()}
                  </span>
                </div>

                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>
                    {product.transaction_count?.toLocaleString()} transactions
                  </span>
                  <span>
                    Avg: ${product.avg_cost_per_transaction?.toLocaleString()}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.cost_by_supplier && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Cost by Supplier
          </h3>
          <ul className="mt-4 space-y-4">
            {data.cost_by_supplier?.slice(0, 5).map((supplier) => (
              <li
                key={supplier?.supplier}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {supplier?.supplier}
                  </span>
                  <span className="font-semibold text-green-400">
                    ${supplier.total_cost?.toLocaleString()}
                  </span>
                </div>

                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>
                    {supplier.transaction_count?.toLocaleString()} transactions
                  </span>
                  <span>
                    Avg: ${supplier.avg_cost_per_transaction?.toLocaleString()}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.cost_by_warehouse && (
        <div>
          <h3 className="text-xl font-semibold text-gray-300">
            Cost by Warehouse
          </h3>
          <ul className="mt-4 space-y-4">
            {data.cost_by_warehouse?.slice(0, 5).map((warehouse) => (
              <li
                key={warehouse?.warehouse}
                className="group rounded-lg bg-gray-800 p-4 transition-colors duration-200 hover:bg-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-400 group-hover:text-gray-200">
                    {warehouse?.warehouse}
                  </span>
                  <span className="font-semibold text-green-400">
                    ${warehouse.total_cost?.toLocaleString()}
                  </span>
                </div>

                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>
                    {warehouse.transaction_count?.toLocaleString()} transactions
                  </span>
                  <span>
                    Avg: ${warehouse.avg_cost_per_transaction?.toLocaleString()}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
