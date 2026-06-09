const MarketStatus = ({indexData,indexDataCSE})=>{
    return (
      <>
        <div className="bg-dark text-light py-2 border-top border-secondary">
          <div className="container d-flex flex-wrap justify-content-center text-center">
            <span className="me-4 text-warning">
              Tr: DSE: {indexData?.trade ?? "-"} | CSE:{" "}
              {indexDataCSE?.trade ?? "-"}
            </span>
            <span className="me-4 text-info">
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