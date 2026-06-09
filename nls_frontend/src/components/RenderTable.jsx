const RenderTable = ({ activeTab, sharePrice }) => {
  const tableColors = {
    Gainer: { headerBg: "#16a34a", headerText: "#fff", bodyBg: "#f0fdf4" },
    Loser: { headerBg: "#dc2626", headerText: "#fff", bodyBg: "#fef2f2" },
    Value: { headerBg: "#2563eb", headerText: "#fff", bodyBg: "#eff6ff" },
    Volume: { headerBg: "#9333ea", headerText: "#fff", bodyBg: "#faf5ff" },
  };

  const { headerBg, headerText, bodyBg } =
    tableColors[activeTab] || tableColors.Value;

  const showChangeColumns = !(activeTab === "Value" || activeTab === "Volume");
  const valueHeader = activeTab === "Value" ? "Value(mn)" : "Volume";

  return (
    <div className="table-responsive">
      <table className="table table-bordered">
        <thead style={{ backgroundColor: headerBg, color: headerText }}>
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

        <tbody style={{ backgroundColor: bodyBg }}>
          {sharePrice &&
            sharePrice.slice(0, 10).map((item, index) => (
              <tr key={index}>
                <td>{item.symbol}</td>
                <td>{item.ltp}</td>
                <td>{item.ycp}</td>

                {showChangeColumns ? (
                  <>
                    <td>{item.change_val}</td>
                    <td>{item.change_per}</td>
                  </>
                ) : activeTab === "Value" ? (
                  <td>{item.value_mn}</td>
                ) : (
                  <td>{item.volume}</td>
                )}
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default RenderTable;