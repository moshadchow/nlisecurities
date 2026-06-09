import { useEffect, useState } from "react";
import { fetchTickerPrice } from "../services/chartService";

const Ticker = () => {
  const [mergedData, setMergedData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    let interval;

    const loadData = async () => {
      try {
        const dseData = await fetchTickerPrice("DSE");
        const cseData = await fetchTickerPrice("CSE");
        if (dseData.error) throw new Error(dseData.error);
        if (cseData.error) throw new Error(cseData.error);
        if ((!dseData || dseData.length === 0) && (!cseData || cseData.length === 0)) {
          throw new Error("Empty response from both sources");
        }

        // Merge both datasets by instrument
        const combined = {};
        dseData.forEach((item) => {
          combined[item.inst] = { inst: item.inst, DSE: item };
        });
        cseData.forEach((item) => {
          if (!combined[item.inst]) combined[item.inst] = { inst: item.inst };
          combined[item.inst].CSE = item;
        });

        setMergedData(Object.values(combined));
      } catch (err) {
        setError(err.message);
        setMergedData(null);
      }
    };

    loadData();

    // auto-refresh every 10 seconds
    interval = setInterval(loadData, 10000);

    // cleanup on unmount
    return () => clearInterval(interval);
  }, []);
  { error && <div className="alert alert-warning text-center">⚠️ {error}</div>; }
  return (
    <marquee behavior="scroll" direction="left" scrollamount="12">
      {!error && mergedData.length > 0 ? (
        mergedData.map((item, i) => (
          <div key={i} style={{ display: "inline-block", marginRight: "25px", color: "#ffffff" }}>
            <strong>{item.inst}</strong>{" "}
            {item.DSE ? (
              <span
                style={{
                  color:
                    item.DSE.arrow === "tkup"
                      ? "#39ff14"
                      : item.DSE.arrow === "tkdown"
                        ? "#ff6b6b"
                        : "#ffd700",
                }}
              >
                | DSE: {item.DSE.price} ({item.DSE.percent})
              </span>
            ) : (
              " | DSE: —"
            )}
            {item.CSE ? (
              <span
                style={{
                  color:
                    item.CSE.arrow === "tkup"
                      ? "#39ff14"
                      : item.CSE.arrow === "tkdown"
                        ? "#ff6b6b"
                        : "#ffd700",
                }}
              >
                {" "}
                | CSE: {item.CSE.price} ({item.CSE.percent})
              </span>
            ) : (
              " | CSE: —"
            )}
          </div>
        ))
      ) : (
        <div className="text-center p-5">
          <div className="spinner-border text-primary mb-3" role="status"></div>
        </div>
      )}
    </marquee>
  );
};

export default Ticker;
