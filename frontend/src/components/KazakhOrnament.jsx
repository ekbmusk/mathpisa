export function QoshkarMuyiz({ size = 64, className = '', color = 'currentColor', strokeWidth = 1.3, opacity = 1 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 80 80"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ opacity }}
    >
      <g stroke={color} strokeWidth={strokeWidth} fill="none" strokeLinecap="round" strokeLinejoin="round">
        {/* upper horn spiral */}
        <path d="M40 12 C28 12 22 22 22 32 C22 40 28 46 34 46 C38 46 40 44 40 40 C40 36 38 34 36 34 C34 34 33 36 34 37" />
        {/* lower horn spiral, mirrored */}
        <path d="M40 68 C52 68 58 58 58 48 C58 40 52 34 46 34 C42 34 40 36 40 40 C40 44 42 46 44 46 C46 46 47 44 46 43" />
        {/* central node */}
        <circle cx="40" cy="40" r="1.6" fill={color} stroke="none" />
        {/* outer arc accents */}
        <path d="M14 40 Q8 40 8 34" opacity="0.6" />
        <path d="M66 40 Q72 40 72 46" opacity="0.6" />
      </g>
    </svg>
  )
}

export function RhombusBand({ width = 200, height = 12, className = '', color = 'currentColor', opacity = 0.6 }) {
  const diamonds = Math.floor(width / 14)
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ opacity }}
    >
      {Array.from({ length: diamonds }).map((_, i) => {
        const cx = 7 + i * 14
        return (
          <g key={i}>
            <path
              d={`M${cx} 2 L${cx + 5} ${height / 2} L${cx} ${height - 2} L${cx - 5} ${height / 2} Z`}
              stroke={color}
              strokeWidth="0.9"
              fill="none"
            />
            <circle cx={cx} cy={height / 2} r="0.9" fill={color} />
          </g>
        )
      })}
    </svg>
  )
}

export function ArchFrame({ size = 120, className = '', color = 'currentColor', opacity = 0.25 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 120 120"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ opacity }}
    >
      <g stroke={color} strokeWidth="0.9" fill="none">
        <path d="M10 110 L10 50 Q10 10 60 10 Q110 10 110 50 L110 110" />
        <path d="M20 110 L20 55 Q20 20 60 20 Q100 20 100 55 L100 110" opacity="0.5" />
        <circle cx="60" cy="40" r="4" />
        <path d="M52 40 L68 40 M60 32 L60 48" strokeLinecap="round" />
      </g>
    </svg>
  )
}
