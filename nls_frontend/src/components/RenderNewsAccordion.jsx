const RenderNewsAccordion = ({news, market}) => {
    if (!news || !news.length) {
      return (
        <div className="text-center p-5">
          <div className="spinner-border text-primary mb-3" role="status"></div>
          <p className="text-muted">Loading {market} News...</p>
        </div>
      );
    }

    return (
      <div className="accordion" id={`${market}-accordion`}>
        {news.map((item, index) => {
          const headingId = `${market}-heading-${index}`;
          const collapseId = `${market}-collapse-${index}`;
          const showClass = index === 0 ? "show" : "";

          return (
            <div className="accordion-item" key={index}>
              <h2 className="accordion-header" id={headingId}>
                <button
                  className={`accordion-button ${
                    index !== 0 ? "collapsed" : ""
                  }`}
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target={`#${collapseId}`}
                  aria-expanded={index === 0 ? "true" : "false"}
                  aria-controls={collapseId}
                >
                  {item["title"]} &nbsp;&nbsp; | &nbsp;{" "}
                  <small className="text-muted">
                    {new Date(item["publish_date"]).toLocaleDateString("en-GB")}
                  </small>
                </button>
              </h2>
              <div
                id={collapseId}
                className={`accordion-collapse collapse ${showClass}`}
                aria-labelledby={headingId}
                data-bs-parent={`#${market}-accordion`}
              >
                <div className="accordion-body">
                  <strong>{item["trading_code"]}:</strong> {item["news"]}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  export default RenderNewsAccordion;