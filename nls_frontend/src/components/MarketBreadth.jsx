const MarketBreadth = ({ title, data }) => {
  if (!data) {
    return (
      <div className="hero-market-group">
        <div className="hero-market-group-title">{title}</div>
        <div className="text-center p-4">
          <div
            className="spinner-border text-primary mb-3"
            role="status"
          ></div>
        </div>
      </div>
    );
  }

  return (
    <div className="hero-market-group">
      <div className="hero-market-group-title">{title}</div>
      <div className="market-breadth-cards">
        <div className="stat-card">
          <div className="label">Advance</div>
          <div className="value advance">{data.advance ?? "-"}</div>
        </div>
        <div className="stat-card">
          <div className="label">Decline</div>
          <div className="value decline">{data.decline ?? "-"}</div>
        </div>
        <div className="stat-card">
          <div className="label">Unchanged</div>
          <div className="value unchanged">{data.unchange ?? "-"}</div>
        </div>
      </div>
    </div>
  );
};

export default MarketBreadth;