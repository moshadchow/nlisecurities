import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend,ResponsiveContainer } from 'recharts';

const SectorContainer = ({ title, data, metric }) => {
  const dataKey1 = metric === "volume" ? "DSE_Volume" : "DSE_Value";
  const dataKey2 = metric === "volume" ? "CSE_Volume" : "CSE_Value";

  return (
    <div className="card shadow-sm p-3 rounded-3">
      <h5 className="text-center mb-3">{title}</h5>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 95 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="sector" angle={-30} textAnchor="end" interval={0} />
          <YAxis />
          <Tooltip />
          <Legend
            verticalAlign="top"
            align="right"
            wrapperStyle={{ top: 0, right: 0 }}
          />
          <Bar dataKey={dataKey1} fill="#007bff" name="DSE" />
          <Bar dataKey={dataKey2} fill="#28a745" name="CSE" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SectorContainer;