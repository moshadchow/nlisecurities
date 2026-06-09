import Breadcrumbs from '../components/Breadcrumbs'
import {useState, useEffect } from "react";
// import { fetchDSENews,fetchCSENews } from '../services/chartService';

import RenderNewsAccordion from "../components/RenderNewsAccordion"
import { getMarketNews } from '../services/getApi';

function MarketNews(){
  const [dseNews, setDseNews] = useState([]);
  const [cseNews, setCseNews] = useState([]);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("DSE");

    useEffect(()=>{
        let interval;
        const fetchMarketData = async () => {
        try {
            const dseNews = await getMarketNews('DSE') // Pass the id to API
            const cseNews = await getMarketNews('CSE')
            setDseNews(dseNews);
            setCseNews(cseNews);
        } catch (err) {
            setError(err.message);
        } 
        };
        fetchMarketData()
        // Set interval to refresh every 10 seconds
        interval = setInterval(() => {
          fetchMarketData();
        }, 120000); // 10,000 ms = 10 sec
        // Cleanup interval on component unmount
        return () => clearInterval(interval);
    },[])

return (
  <>
    <Breadcrumbs folder="Pages" page="Market News" />
    <div className="container-fluid py-4">
      <div className="container">
        {error && (
          <div className="alert alert-danger text-center" role="alert">
            {error}
          </div>
        )}

        {/* Tabs */}
        <ul className="nav nav-tabs mb-4 justify-content-center" role="tablist">
          <li className="nav-item" role="presentation">
            <button
              className={`nav-link ${activeTab === "DSE" ? "active" : ""}`}
              onClick={() => setActiveTab("DSE")}
              type="button"
              role="tab"
            >
              DSE News
            </button>
          </li>
          <li className="nav-item" role="presentation">
            <button
              className={`nav-link ${activeTab === "CSE" ? "active" : ""}`}
              onClick={() => setActiveTab("CSE")}
              type="button"
              role="tab"
            >
              CSE News
            </button>
          </li>
        </ul>

        {/* Tab Content */}
        <div className="tab-content">
          <div
            className={`tab-pane fade ${
              activeTab === "DSE" ? "show active" : ""
            }`}
            role="tabpanel"
          >
            <RenderNewsAccordion news={dseNews} market="DSE" />
          </div>
          <div
            className={`tab-pane fade ${
              activeTab === "CSE" ? "show active" : ""
            }`}
            role="tabpanel"
          >
            <RenderNewsAccordion news={cseNews} market="CSE" />
          </div>
        </div>
      </div>
    </div>
  </>
);
}
export default MarketNews