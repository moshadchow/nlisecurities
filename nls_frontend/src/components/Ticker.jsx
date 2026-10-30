import { useEffect, useState } from "react";
import { fetchTickerPrice } from "../services/chartService";

const TickerItem = ({ item }) => (
  <div className="ticker-item">
    <strong>{item.inst}</strong>{" "}
    {item.DSE ? (
      <span className={item.DSE.arrow === "tkup" ? "text-up" : item.DSE.arrow === "tkdown" ? "text-down" : "text-neutral"}>
        | DSE: {item.DSE.price} ({item.DSE.percent})
      </span>
    ) : (
      " | DSE: —"
    )}
    {item.CSE ? (
      <span className={item.CSE.arrow === "tkup" ? "text-up" : item.CSE.arrow === "tkdown" ? "text-down" : "text-neutral"}>
        {" "}
        | CSE: {item.CSE.price} ({item.CSE.percent})
      </span>
    ) : (
      " | CSE: —"
    )}
  </div>
);

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

    interval = setInterval(loadData, 10000);

    return () => clearInterval(interval);
  }, []);

  { error && <div className="alert alert-warning text-center">⚠️ {error}</div>; }
  return (
    <div className="ticker-wrap">
      <div className="ticker-track">
        {!error && mergedData.length > 0 ? (
          <>
            {mergedData.map((item, i) => (
              <TickerItem key={i} item={item} />
            ))}
            {mergedData.map((item, i) => (
              <TickerItem key={i + 1000} item={item} />
            ))}
          </>
        ) : (
          <div className="ticker-item text-center p-5">
            <div className="spinner-border text-primary mb-3" role="status"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Ticker;
