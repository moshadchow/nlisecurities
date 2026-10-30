const IndexTable = ({ title, indices, indexData }) => {
  if (!indexData) {
    return (
      <div className="hero-index-table-wrap">
        <div className="hero-index-table-title">{title}</div>
        <div className="text-center p-5">
          <div
            className="spinner-border text-primary mb-3"
            role="status"
          ></div>
        </div>
      </div>
    );
  }

  const rows = indices
    .map((key) => indexData.find((item) => item.index === key))
    .filter(Boolean);

  const getChangeClass = (arrow) => {
    if (arrow === "upArrow") return "text-up";
    if (arrow === "downArrow") return "text-down";
    return "text-neutral";
  };

  const formatChange = (item) => {
    if (!item) return "-";
    const change = item.change;
    if (change === null || change === undefined) return "-";
    const sign = change > 0 ? "+" : change < 0 ? "" : "";
    return `${sign}${change}`;
  };

  const formatPercent = (item) => {
    if (!item) return "-";
    const pct = item.percent;
    if (pct === null || pct === undefined) return "-";
    const sign = pct > 0 ? "+" : pct < 0 ? "" : "";
    return `${sign}${pct}%`;
  };

  return (
    <div className="hero-index-table-wrap">
      <div className="hero-index-table-title">{title}</div>
      <div className="table-responsive">
        <table className="table table-bordered">
          <thead>
            <tr>
              <th>Index</th>
              <th>Index Value</th>
              <th>Index Change</th>
              <th>Change (%)</th>
            </tr>
          </thead>
          <tbody>
            {rows.length > 0 ? (
              rows.map((item, i) => (
                <tr key={item.index || i}>
                  <td>{item.index}</td>
                  <td>{item.value ?? "-"}</td>
                  <td className={getChangeClass(item.arrow)}>
                    {formatChange(item)}
                  </td>
                  <td className={getChangeClass(item.arrow)}>
                    {formatPercent(item)}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4">
                  <div className="text-center p-4 text-muted">
                    No data available
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default IndexTable;