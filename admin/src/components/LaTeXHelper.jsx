const FORMULAS = ['ax^2 + bx + c = 0', 'x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}', 'S = \\pi r^2', 'P = \\frac{f}{n}', '\\bar{x} = \\frac{\\sum x_i}{n}']

export default function LaTeXHelper({ onInsert }) {
    return (
        <div className="flex flex-wrap gap-2">
            {FORMULAS.map((formula) => (
                <button
                    key={formula}
                    className="rounded-lg border border-border bg-surface-2 px-2.5 py-1.5 text-xs text-text-2 hover:text-text-1"
                    onClick={() => onInsert?.(formula)}
                    type="button"
                >
                    {formula}
                </button>
            ))}
        </div>
    )
}