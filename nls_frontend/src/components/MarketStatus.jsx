const MarketStatus = ({indexData,indexDataCSE})=>{
    return (
      <>
        <div className="market-status-bar py-2">
          <div className="container d-flex flex-wrap justify-content-center text-center gap-3">
            <span className="text-muted">
              Tr: DSE: {indexData?.trade ?? "-"} | CSE:{" "}
              {indexDataCSE?.trade ?? "-"}
            </span>
            <span className="text-info">
              Vol: DSE: {indexData?.volume ?? "-"} | CSE:{" "}
              {indexDataCSE?.volume ?? "-"}
            </span>
            <span className="text-light">
              Val: DSE: {indexData?.value ?? "-"} | CSE:{" "}
              {indexDataCSE?.value ?? "-"}
            </span>
          </div>
        </div>
      </>
    );
}

export default MarketStatus;
