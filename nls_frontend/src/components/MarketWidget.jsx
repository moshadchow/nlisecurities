const MarketStatCard = ({ label, value, variant }) => {
  const displayValue = value !== null && value !== undefined ? value : "-";
  return (
    <div className="stat-card">
      <div className="label">{label}</div>
      <div className={`value ${variant}`}>{displayValue}</div>
    </div>
  );
};

const IndexStatCard = ({ label, indexData, indexKey }) => {
  const entry = Array.isArray(indexData)
    ? indexData.find((item) => item.index === indexKey)
    : null;

  if (!entry) {
    return (
      <div className="stat-card">
        <div className="label">{label}</div>
        <div className="value">-</div>
      </div>
    );
  }

  const isUp = entry.arrow === "upArrow";
  const isDown = entry.arrow === "downArrow";
  const changeClass = isUp ? "advance" : isDown ? "decline" : "unchanged";

  return (
    <div className="stat-card index-card">
      <div className="label">{label}</div>
      <div className="value">{entry.value}</div>
      <div className={`change ${changeClass}`}>
        {entry.change} ({entry.percent}%)
      </div>
    </div>
  );
};

export { MarketStatCard, IndexStatCard };