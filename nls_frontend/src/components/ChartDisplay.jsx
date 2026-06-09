import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";


const AreaChartDisplay = ({ type, data }) => {
  // Fallback for missing data
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[350px] text-gray-500">
        No data available.
      </div>
    );
  }

  // --- X-Axis hourly tick logic ---
  const hourlyTicks = data
    .filter((d, i, arr) => i === 0 || d.time.slice(0, 2) !== arr[i - 1].time.slice(0, 2))
    .map((d) => d.time);

  // --- Y-Axis range setup ---
  const values = data.map((d) => d.index);
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  const startValue = Math.floor(minValue / 5) * 5;

  const yTicks = [];
  for (let v = startValue; v <= maxValue + 5; v += 5) {
    yTicks.push(v);
  }
  const CHART_COLORS = {
    DSEX: { stroke: "#2563eb", fill: "#93c5fd" },   // blue
    DSES: { stroke: "#16a34a", fill: "#86efac" },   // green
    DS30: { stroke: "#ea580c", fill: "#fdba74" },   // orange
    CDSET: { stroke: "#9333ea", fill: "#d8b4fe" },  // purple

    CSE50: { stroke: "#15803d", fill: "#86efac" },  // dark green
    CSE30: { stroke: "#0891b2", fill: "#67e8f9" },  // teal
    CSCX:  { stroke: "#ca8a04", fill: "#fde68a" },  // gold
    CASPI: { stroke: "#7c3aed", fill: "#c4b5fd" },  // violet
    CSI:   { stroke: "#db2777", fill: "#f9a8d4" }   // pink
  };
  // --- Pick color by type (default to blue if unknown type) ---
  const { stroke, fill } = CHART_COLORS[type] || CHART_COLORS.DSEX;

  return (
    <div style={{ width: "100%", height: 350 }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="time"
            ticks={hourlyTicks}
            tickFormatter={(val) => val.slice(0, 2)}
            label={{ value: "Hour", position: "insideBottomRight", offset: 1 }}
          />
          <YAxis
            ticks={yTicks}
            domain={[startValue, maxValue + 5]}
            label={{ value: "Index", angle: -90, position: "insideLeft" }}
          />
          <Tooltip />
          <Area
            type="monotone"
            dataKey="index"
            stroke={stroke}
            fill={fill}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AreaChartDisplay;
