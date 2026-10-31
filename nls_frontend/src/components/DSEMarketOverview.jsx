import MarketBreadth from "./MarketBreadth";
import IndexTable from "./IndexTable";

const DSEMarketOverview = ({ breadthData, indexData }) => {
  return (
    <div className="hero-market-group dse-overview-group">
      <MarketBreadth
        title="Dhaka Stock Exchange (DSE)"
        data={breadthData}
      />
      <div className="mt-3">
        <IndexTable
          title="DSE Indices"
          indices={["DSEX", "DS30", "DSES"]}
          indexData={indexData}
        />
      </div>
    </div>
  );
};

export default DSEMarketOverview;