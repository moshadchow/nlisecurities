import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { getPlainText, getFeatures, getEvents } from "../services/getApi";
import { fetchMarketInfo, fetchMarketIndex, fetchTopSharePrice } from "../services/chartService";

import HeroSlider from '../components/HeroSlider';
import SplashScreen from '../components/SplashScreen';
import FaqSection from '../components/FaqSection';
import FeatureCard from '../components/FeatureCard';
import MarketBreadth from '../components/MarketBreadth';
import IndexTable from '../components/IndexTable';
import CSEMarketOverview from '../components/CSEMarketOverview';
import MarketPerformanceTable from '../components/MarketPerformanceTable';


function Home() {
  const [error, setError] = useState(null);
  const [marketBreadthDSE, setMarketBreadthDSE] = useState(null);
  const [marketBreadthCSE, setMarketBreadthCSE] = useState(null);
  const [indexValues, setIndexValues] = useState(null);
  const [indexValuesCSE, setIndexValuesCSE] = useState(null);
  const [dseShareData, setDseShareData] = useState(null);
  const [cseShareData, setCseShareData] = useState(null);
  const [features, setFeatures] = useState(null);
  const [events, setEvents] = useState(null);

  useEffect(() => {
    const loadFeatures = async () => {
      try {
        const response = await getFeatures(null);
        if (response.error) throw new Error(response.error);
        setFeatures(response);
      } catch (err) {
        setError(err.message);
        setFeatures(null);
      }
    };

    const loadEvents = async () => {
      try {
        const response = await getEvents(null);
        if (response.error) throw new Error(response.error);
        setEvents(response);
      } catch (err) {
        setError(err.message);
        setFeatures(null);
      }
    };

    const loadMarketIndex = async () => {
      try {
        const breadthDSE = await fetchMarketInfo("DSE");
        const breadthCSE = await fetchMarketInfo("CSE");
        const idxResponse = await fetchMarketIndex("DSE");
        const idxResponseCSE = await fetchMarketIndex("CSE");
        const dseShares = await fetchTopSharePrice("DSE");
        const cseShares = await fetchTopSharePrice("CSE");
        if (breadthDSE.error) throw new Error(breadthDSE.error);
        if (breadthCSE.error) throw new Error(breadthCSE.error);
        if (idxResponse.error) throw new Error(idxResponse.error);
        if (idxResponseCSE.error) throw new Error(idxResponseCSE.error);
        if (dseShares.error) throw new Error(dseShares.error);
        if (cseShares.error) throw new Error(cseShares.error);
        setMarketBreadthDSE(breadthDSE);
        setMarketBreadthCSE(breadthCSE);
        setIndexValues(idxResponse);
        setIndexValuesCSE(idxResponseCSE);
        setDseShareData(dseShares);
        setCseShareData(cseShares);
      } catch (err) {
        setError(err.message);
        setMarketBreadthDSE(null);
        setMarketBreadthCSE(null);
        setIndexValues(null);
        setIndexValuesCSE(null);
        setDseShareData(null);
        setCseShareData(null);
      }
    };

    loadFeatures();
    loadEvents();
    loadMarketIndex();

    const interval = setInterval(() => {
      loadMarketIndex();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  { error && <div className="alert alert-warning text-center">⚠️ {error}</div>; }
  return (
    <div>
      <SplashScreen />
      {/* ===== HERO SECTION START ===== */}
      <div className="container-fluid hero-header bg-light">
        <div className="container-fluid">
          <HeroSlider />
        </div>
        <div className="container py-3">
          <div className="row g-3 hero-market-dashboard-row align-items-start">
            {/* Group 1: DSE Market Breadth */}
            <div className="col-12 col-lg-3 col-xl-2">
              <MarketBreadth
                title="Dhaka Stock Exchange (DSE)"
                data={marketBreadthDSE}
              />
            </div>
            {/* Group 2: DSE Index Table */}
            <div className="col-12 col-lg-4 col-xl-5">
              <IndexTable
                title="DSE Indices"
                indices={["DSEX", "DS30", "DSES"]}
                indexData={indexValues}
              />
            </div>
            {/* Group 3: CSE Market Breadth + Index Table */}
            <div className="col-12 col-lg-5 col-xl-5">
              <CSEMarketOverview
                breadthData={marketBreadthCSE}
                indexData={indexValuesCSE}
              />
            </div>
          </div>
        </div>
      </div>
      {/* ===== HERO END ===== */}
      {/* Hero End */}
      {/* Chart Start - Market Performance Tables */}
      <div className="container-fluid py-5 bg-dark">
        <div className="container">
          <div className="text-center wow fadeIn" data-wow-delay="0.1s">
            <h1 className="mb-4 text-primary bg-light">
              Market{" "}
              <span className="text-uppercase px-2">
                (At a Glance)
              </span>
            </h1>
          </div>

          {/* DSE Market Performance Tables */}
          <div className="market-performance-section mb-5">
            <h3 className="text-primary mb-4">Dhaka Stock Exchange (DSE)</h3>
            <div className="row g-4">
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="DSE Gainers"
                  data={dseShareData}
                  category="gainer"
                />
              </div>
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="DSE Losers"
                  data={dseShareData}
                  category="loser"
                />
              </div>
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="DSE Highest Value"
                  data={dseShareData}
                  category="value"
                />
              </div>
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="DSE Highest Volume"
                  data={dseShareData}
                  category="volume"
                />
              </div>
            </div>
          </div>

          {/* CSE Market Performance Tables */}
          <div className="market-performance-section">
            <h3 className="text-primary mb-4">Chittagong Stock Exchange (CSE)</h3>
            <div className="row g-4">
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="CSE Gainers"
                  data={cseShareData}
                  category="gainer"
                />
              </div>
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="CSE Losers"
                  data={cseShareData}
                  category="loser"
                />
              </div>
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="CSE Highest Value"
                  data={cseShareData}
                  category="value"
                />
              </div>
              <div className="col-12 col-lg-6">
                <MarketPerformanceTable
                  title="CSE Highest Volume"
                  data={cseShareData}
                  category="volume"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Chart End */}
      {/* Feature Start */}
      <div className="container-fluid py-5 feature-section">
        <div className="container py-5">
          <div className="text-center mb-5">
            <h2 className="feature-section-title">
              Why Investor{" "}
              <span className="text-teal">Choose Us</span>
            </h2>
          </div>
          <div className="row g-4 feature-card-grid">
            {features &&
              features.map((item, index) => {
                const icons = [
                  "fa-calendar-alt",
                  "fa-tasks",
                  "fa-pencil-ruler",
                  "fa-user",
                  "fa-hand-holding-usd",
                  "fa-check",
                ];
                return (
                  <div key={item.id ?? index} className="col-12 col-md-6 col-lg-4">
                    <FeatureCard
                      title={item.title}
                      description={item.description}
                      iconClass={icons[index]}
                    />
                  </div>
                );
              })}
          </div>
        </div>
      </div>
      {/* Feature End */}
      {/*Events Start */}
      <div className="container-fluid bg-primary newsletter p-0">
        <div className="container py-5">
          <h1 className="text-center mb-5 fw-bold">Our Recent Events</h1>
          <div className="row g-4">
            {events &&
              events.map((event, index) => (
                <div className="col-md-6 col-lg-4" key={index}>
                  <div className="card h-100 shadow-sm border-0">
                    <img
                      src={
                        event
                          ? "http://127.0.0.1:8000" + event.image
                          : "No Image"
                      }
                      className="card-img-top"
                      alt={event.title}
                      style={{ height: "230px", objectFit: "cover" }}
                    />
                    <div className="card-body">
                      <h5 className="card-title fw-semibold">{event.title}</h5>
                      <p className="card-text text-muted small">
                        {getPlainText(event.description)}
                      </p>
                    </div>
                    <div className="card-footer bg-white border-0 text-end">
                      <Link
                        to={`/event_dtl/${event.id}`}
                        className="btn btn-outline-primary btn-sm"
                      >
                        Read More
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
      {/* Events End */}
      {/* FAQ Section */}
      <FaqSection />
      {/* FAQ Section End */}
      {/* Back to Top */}
      <Link
        to="#!"
        className="btn btn-lg btn-primary btn-lg-square back-to-top"
      >
        <i className="bi bi-arrow-up"></i>
      </Link>
    </div>
  );
}
export default Home;
