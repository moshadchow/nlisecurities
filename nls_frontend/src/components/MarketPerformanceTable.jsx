const MarketPerformanceTable = ({ title, data, category }) => {
  if (!data) {
    return (
      <div className="market-performance-table-wrap">
        <div className="market-performance-title">{title}</div>
        <div className="text-center p-5">
          <div
            className="spinner-border text-primary mb-3"
            role="status"
          ></div>
        </div>
      </div>
    );
  }

  const sorted = [...data].sort((a, b) => {
    const changeA = parseFloat(a.change_per) || 0;
    const changeB = parseFloat(b.change_per) || 0;
    const valueA = parseFloat(a.value_mn) || 0;
    const valueB = parseFloat(b.value_mn) || 0;
    const volumeA = parseFloat(a.volume) || 0;
    const volumeB = parseFloat(b.volume) || 0;

    switch (category) {
      case "gainer":
        return changeB - changeA;
      case "loser":
        return changeA - changeB;
      case "value":
        return valueB - valueA;
      case "volume":
        return volumeB - volumeA;
      default:
        return 0;
    }
  });

  const topItems = sorted.slice(0, 10);

  const getChangeClass = (changePer) => {
    const val = parseFloat(changePer) || 0;
    if (val > 0) return "text-up";
    if (val < 0) return "text-down";
    return "text-neutral";
  };

  const formatChange = (item) => {
    const val = parseFloat(item.change_val);
    if (isNaN(val)) return "-";
    const sign = val > 0 ? "+" : val < 0 ? "" : "";
    return `${sign}${val}`;
  };

  const formatPercent = (item) => {
    const val = parseFloat(item.change_per);
    if (isNaN(val)) return "-";
    const sign = val > 0 ? "+" : val < 0 ? "" : "";
    return `${sign}${val}%`;
  };

  const showChangeColumns = !(category === "value" || category === "volume");
  const valueHeader = category === "value" ? "Value(mn)" : "Volume";

  return (
    <div className="market-performance-table-wrap">
      <div className="market-performance-title">{title}</div>
      <div className="table-responsive">
        <table className="table table-bordered">
          <thead>
            <tr>
              <th>Instrument</th>
              <th>LTP</th>
              <th>YCP</th>
              {showChangeColumns ? (
                <>
                  <th>Change</th>
                  <th>Change(%)</th>
                </>
              ) : (
                <th>{valueHeader}</th>
              )}
            </tr>
          </thead>
          <tbody>
            {topItems.length > 0 ? (
              topItems.map((item, index) => (
                <tr key={index}>
                  <td>{item.symbol}</td>
                  <td>{item.ltp}</td>
                  <td>{item.ycp}</td>
                  {showChangeColumns ? (
                    <>
                      <td className={getChangeClass(item.change_per)}>
                        {formatChange(item)}
                      </td>
                      <td className={getChangeClass(item.change_per)}>
                        {formatPercent(item)}
                      </td>
                    </>
                  ) : category === "value" ? (
                    <td>{item.value_mn}</td>
                  ) : (
                    <td>{item.volume}</td>
                  )}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5}>
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

export default MarketPerformanceTable;