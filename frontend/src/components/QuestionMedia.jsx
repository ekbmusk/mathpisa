import { useState } from 'react'
import FormulaRenderer from './FormulaRenderer'

export default function QuestionMedia({ imageUrl, tableData }) {
  const [imgError, setImgError] = useState(false)

  if (!imageUrl && !tableData) return null

  return (
    <>
      {imageUrl && !imgError && (
        <div className="my-2 rounded-xl overflow-hidden border border-border bg-surface-2">
          <img
            src={imageUrl}
            alt="Сурет"
            className="w-full max-h-60 object-contain"
            loading="lazy"
            onError={() => setImgError(true)}
          />
        </div>
      )}
      {tableData?.headers && tableData?.rows && (
        <div className="my-2 overflow-x-auto rounded-xl border border-border">
          {tableData.caption && (
            <p className="text-[10px] text-text-3 px-2.5 pt-1.5 pb-0.5">{tableData.caption}</p>
          )}
          <table className="w-full text-xs text-text-1">
            <thead>
              <tr className="bg-surface-2">
                {tableData.headers.map((h, i) => (
                  <th key={i} className="px-2.5 py-1.5 text-left font-semibold text-text-2 border-b border-border whitespace-nowrap">
                    <FormulaRenderer formula={h} />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.rows.map((row, ri) => (
                <tr key={ri} className="border-b border-border/50 last:border-0">
                  {row.map((cell, ci) => (
                    <td key={ci} className="px-2.5 py-1.5 whitespace-nowrap">
                      <FormulaRenderer formula={cell} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  )
}
