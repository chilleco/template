export function DataTable({ data, columns }: any) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr>
            {columns?.map((column: any, index: number) => (
              <th key={index} className="border border-gray-300 p-2 bg-gray-100">
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data?.map((row: any, rowIndex: number) => (
            <tr key={rowIndex}>
              {columns?.map((column: any, colIndex: number) => (
                <td key={colIndex} className="border border-gray-300 p-2">
                  {column.cell ? column.cell({ getValue: () => row[column.accessorKey] }) : row[column.accessorKey]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
} 