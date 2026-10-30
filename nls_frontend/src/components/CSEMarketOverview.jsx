import MarketBreadth from "./MarketBreadth";
import IndexTable from "./IndexTable";

const CSEMarketOverview = ({ breadthData, indexData }) => {
  return (
    <div className="hero-market-group cse-overview-group">
      <MarketBreadth
        title="Chittagong Stock Exchange (CSE)"
        data={breadthData}
      />
      <div className="mt-3">
        <IndexTable
          title="CSE Indices"
          indices={["CSCX", "CSE50", "CSE30", "CASPI", "CSI"]}
          indexData={indexData}
        />
      </div>
    </div>
  );
};

export default CSEMarketOverview;