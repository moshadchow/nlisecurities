import { useEffect, useState } from "react";
import { fetchMinutesIndex,fetchMarketIndex,fetchTopSharePrice } from "../services/chartService";
import AreaChartDisplay from "../components/ChartDisplay"
import RenderTable from './RenderTable';
// Index Chart component
const IndexChartCSE = () => {
  const [activeTab, setActiveTab] = useState("CSE50");
  const [error, setError] = useState(null);
  const [chartData, setChartData] = useState({
    CSE50: [],
    CSE30: [],
    CSCX: [],
    CASPI:[],
    CSI:[],
  });

  useEffect(() => {
    let interval;
    const loadData = async () => {
       try {
          const response = await fetchMinutesIndex("CSE");
          if (response.error) throw new Error(response.error);
          setChartData(response); // clear any previous data
          } 
          catch (err) {
            setError(err.message);
            setChartData(null); 
          } 
    };
    loadData();
    // Set interval to refresh every 10 seconds
    interval = setInterval(() => {
        loadData();
    }, 10000); // 10,000 ms = 10 sec

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  // useEffect(() => {
  //   console.log("Chart data updated:", chartData);
  // }, [chartData]); // logs when state actually updates

 const getCurrentData = () => {
    switch (activeTab) {
      case "CSE50":
        return chartData.CSE50;
      case "CSE30":
        return chartData.CSE30;
      case "CSCX":
        return chartData.CSCX;
      case "CASPI":
        return chartData.CASPI;
      case "CSI":
        return chartData.CSI;
      default:
        return [];
    }
  };
  {error && <div className="alert alert-warning text-center">⚠️ {error}</div>;}
  return (
    <div className="container mt-4 p-3 bg-white rounded shadow">
      {/* Title */}
      <h4 className="mb-4 text-center text-primary fw-bold">CSE Market Index Overview</h4>
      {/* Tabs */}
      <div className="btn-group w-100 mb-3" role="group">
        {["CSE50", "CSE30", "CSCX", "CASPI", "CSI"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`btn ${
              activeTab === tab ? "btn-primary" : "btn-outline-secondary"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Chart */}
        {chartData ? (
        <AreaChartDisplay type={activeTab} data={getCurrentData()} />
      ) : (
        <div className="text-center p-5">
          <div className="spinner-border text-primary mb-3" role="status"></div>
        </div>
      )}
    </div>
  );
  };

// Index data component
const CSEIndex = () => {
  const [indexData,setIndexData] = useState(null)
  const [error, setError] = useState(null);

  useEffect(()=>{
    let interval;
    const loadData = async ()=>{
       try {
          const response = await fetchMarketIndex("CSE");
          if (response.error) throw new Error(response.error);
          setIndexData(response); // clear any previous data
          } 
          catch (err) {
            setError(err.message);
            setIndexData(null); 
          } 
    }
    loadData()
      // Set interval to refresh every 10 seconds
    interval = setInterval(() => {
      loadData();
    }, 10000); // 10,000 ms = 10 sec

      // Cleanup interval on component unmount
    return () => clearInterval(interval);
    }, []);
  {error && <div className="alert alert-warning text-center">⚠️ {error}</div>;}
  return (
    <>
      <div className="table-responsive">
        <table className="table table-bordered">
          <thead className="table-primary">
            <tr>
              <th>Name</th>
              <th>Index</th>
              <th>value</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            {indexData ? (
              indexData.map((item, index) => (
                <tr key={index} className={"table-warning"}>
                  <td>{item.index}</td>
                  <td>{item.value}</td>
                  <td>{item.change}</td>
                  <td>{item.percent}%</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4">
                  <div className="text-center p-5">
                    <div
                      className="spinner-border text-primary mb-3"
                      role="status"
                    ></div>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}

// Top instrument by category
const FetchTopShareCSEBy = () => {
  const [stocks, setStocks] = useState([]);
  const [activeTab, setActiveTab] = useState("Gainer");
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Step 1: Fetch the JSON data from external URL
        const data = await fetchTopSharePrice("CSE")
        if (data.error) throw new Error(data.error);
        // Step 2: Calculate change_per for each item
        const withChangePer = data.map((item) => {
          const change_val = parseFloat(item.change_val);
          const ycp = parseFloat(item.ycp);
          const change_per = (change_val / ycp) * 100;
          return { ...item, change_per: change_per.toFixed(2) };
        });

        setStocks(withChangePer);
      } catch (err) {
        setError(err.message);
        setStocks(null); 
      } 
    };

    // Call the async function
    fetchData();
  }, []);

    // Sort dynamically based on tab
  const getSortedData = () => {
      if (activeTab === "Gainer") {
        return [...stocks].sort((a, b) => b.change_per - a.change_per);
      } else if (activeTab === "Loser") {
        return [...stocks].sort((a, b) => a.change_per - b.change_per);
      } else if (activeTab === "Value") {
        return [...stocks].sort((a, b) => b.value_mn - a.value_mn);
      } else if (activeTab === "Volume") {
        return [...stocks].sort((a, b) => b.volume - a.volume);
      }
      return stocks;
    };

    const sortedData = getSortedData();
    {error && <div className="alert alert-warning text-center">⚠️ {error}</div>;}
    return (
      <>
        <div className="btn-group w-100 mb-3" role="group">
          {["Gainer", "Loser", "Value", "Volume"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`btn ${
                activeTab === tab ? "btn-primary" : "btn-outline-secondary"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
        {stocks ? (
          <RenderTable activeTab={activeTab} sharePrice={sortedData} />
        ) : (
          <div className="text-center p-5">
            <div
              className="spinner-border text-primary mb-3"
              role="status"
            ></div>
          </div>
        )}
      </>
    );
  }
export default IndexChartCSE;
export { CSEIndex,FetchTopShareCSEBy };
