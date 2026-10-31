const EXCHANGES = [
  { id: "DSE", label: "DSE – Dhaka Stock Exchange" },
  { id: "CSE", label: "CSE – Chittagong Stock Exchange" },
];

const CATEGORIES = [
  { id: "gainer", label: "Gainers" },
  { id: "loser", label: "Losers" },
  { id: "value", label: "Highest Value" },
  { id: "volume", label: "Highest Volume" },
];

const MarketMovers = ({
  exchange,
  category,
  onExchangeChange,
  onCategoryChange,
  dseData,
  cseData,
  loading,
  error,
}) => {
  const getSortedTop10 = (data, cat) => {
    if (!data || !Array.isArray(data) || data.length === 0) return [];

    const numeric = data
      .map((item) => {
        const changeVal = parseFloat(item.change_val) || 0;
        const ycp = parseFloat(item.ycp) || 0;
        const changePer = ycp !== 0 ? (changeVal / ycp) * 100 : 0;

        return {
          ...item,
          _changePer: changePer,
          _changeVal: changeVal,
          _valueMn: parseFloat(item.value_mn) || 0,
          _volume: parseFloat(item.volume) || 0,
        };
      })
      .filter(
        (item) =>
          !(item._changePer === 0 && item._changeVal === 0 && item._valueMn === 0 && item._volume === 0)
      );

    let filtered = [...numeric];

    switch (cat) {
      case "gainer":
        filtered = filtered.filter((item) => item._changePer > 0);
        break;
      case "loser":
        filtered = filtered.filter((item) => item._changePer < 0);
        break;
      default:
        break;
    }

    const sorted = filtered.sort((a, b) => {
      let cmp = 0;
      switch (cat) {
        case "gainer":
          cmp = b._changePer - a._changePer;
          break;
        case "loser":
          cmp = a._changePer - b._changePer;
          break;
        case "value":
          cmp = b._valueMn - a._valueMn;
          break;
        case "volume":
          cmp = b._volume - a._volume;
          break;
        default:
          cmp = 0;
      }
      if (cmp === 0) {
        const sa = (a.symbol || "").toString().toLowerCase();
        const sb = (b.symbol || "").toString().toLowerCase();
        return sa < sb ? -1 : sa > sb ? 1 : 0;
      }
      return cmp;
    });

    return sorted.slice(0, 10);
  };

  const getChangeClass = (item) => {
    const val = item._changePer ?? parseFloat(item.change_per) ?? 0;
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
    const val = item._changePer ?? parseFloat(item.change_per);
    if (isNaN(val)) return "-";
    const sign = val > 0 ? "+" : val < 0 ? "" : "";
    return `${sign}${val.toFixed(2)}%`;
  };

  const currentData = exchange === "DSE" ? dseData : cseData;
  const items = getSortedTop10(currentData, category);

  const showChangeColumns = !(category === "value" || category === "volume");
  const extraHeader = category === "value" ? "Value(mn)" : "Volume";

  return (
    <div className="market-performance-section">
      <div className="text-center mb-4">
        <div className="d-flex flex-wrap justify-content-center gap-2 mb-3">
          {EXCHANGES.map((ex) => (
            <button
              key={ex.id}
              className={`btn btn-sm ${
                exchange === ex.id ? "btn-primary" : "btn-outline"
              }`}
              onClick={() => onExchangeChange(ex.id)}
            >
              {ex.label}
            </button>
          ))}
        </div>
        <div className="d-flex flex-wrap justify-content-center gap-2">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              className={`btn btn-sm ${
                category === cat.id ? "btn-primary" : "btn-outline"
              }`}
              onClick={() => onCategoryChange(cat.id)}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      <div className="market-performance-table-wrap">
        {loading ? (
          <div className="text-center p-5">
            <div className="spinner-border text-primary mb-3" role="status"></div>
            <div className="text-muted">Loading market data...</div>
          </div>
        ) : error ? (
          <div className="alert alert-warning text-center">
            ⚠️ {error}
          </div>
        ) : items.length === 0 ? (
          <div className="text-center p-4 text-muted">
            No data available for the selected category.
          </div>
        ) : (
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
                    <th>{extraHeader}</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {items.map((item, index) => (
                  <tr key={index}>
                    <td>{item.symbol}</td>
                    <td>{item.ltp}</td>
                    <td>{item.ycp}</td>
                    {showChangeColumns ? (
                      <>
                        <td className={getChangeClass(item)}>
                          {formatChange(item)}
                        </td>
                        <td className={getChangeClass(item)}>
                          {formatPercent(item)}
                        </td>
                      </>
                    ) : category === "value" ? (
                      <td>{item.value_mn}</td>
                    ) : (
                      <td>{item.volume}</td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default MarketMovers;