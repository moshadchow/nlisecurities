import { Link } from "react-router-dom";
import IndexChart, {
  DSEIndex,
  FetchTopShareBy,
} from "../components/ChartContainer";
import IndexChartCSE, { CSEIndex, FetchTopShareCSEBy } from "../components/ChartContainerCSE";
import { useState, useEffect } from "react";
import { getPlainText, getFeatures, getEvents } from "../services/getApi";
import { fetchMarketInfo } from "../services/chartService";

import IssueStatus from '../components/IssueStatus';
import HeroSlider from '../components/HeroSlider';


function Home() {
  const [error, setError] = useState(null);
  const [indexData, setIndexData] = useState(null);
  const [indexDataCSE, setIndexDataCSE] = useState(null);
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
        setEvents(null);
      }
    };

    const loadMarketIndex = async () => {
      try {
        const response = await fetchMarketInfo("DSE");
        const res_cse = await fetchMarketInfo("CSE");
        if (response.error) throw new Error(response.error);
        if (res_cse.error) throw new Error(res_cse.error);
        setIndexData(response);
        setIndexDataCSE(res_cse);
      } catch (err) {
        setError(err.message);
        setIndexData(null);
        setIndexDataCSE(null);
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
      {/* ===== HERO SECTION START ===== */}
      <div className="container-fluid hero-header bg-light">

        {/* Large Slider First */}
        <div className="container-fluid">
          <HeroSlider />
        </div>
        <div className="container">
          {/* Hero Text Centered */}
          <div className="text-center mb-5">
            <h1 className="display-3 fw-bold">
              We Make Your <span className="text-primary">Invest</span> Better
            </h1>

            <h5 className="border border-2 border-primary d-inline-block py-2 px-4 mt-3">
              A leading capital market service provider Since 2013
            </h5>
          </div>

          {/* Services Row */}
          <div className="row g-5 text-center">
            <div className="col-md-6 col-lg-3">
              <h5>Trade Execution (Buy & Sell Orders)</h5>
            </div>
            <div className="col-md-6 col-lg-3">
              <h5>Client Account Management & Custody Services</h5>
            </div>
            <div className="col-md-6 col-lg-3">
              <h5>Research & Advisory Services</h5>
            </div>
            <div className="col-md-6 col-lg-3">
              <h5>Compliance, Settlement & Reporting</h5>
            </div>
          </div>
        </div>

      </div>
      {/* ===== HERO END ===== */}
      {/* Hero End */}
      {/* Chart Start */}
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
          {/* ===== Market Issue Status HERE ===== */}
          <div className="row justify-content-center mb-5">
            {!error && indexData && indexDataCSE ? (
              <div className="d-flex justify-content-center gap-5 flex-wrap">
                <IssueStatus title="DSE" indexData={indexData} />
                <IssueStatus title="CSE" indexData={indexDataCSE} />
              </div>
            ) : (
              <div className="text-center p-4">
                <div className="spinner-border text-primary"></div>
              </div>
            )}
          </div>
          <div className="row g-5">
            <div className="col-lg-6 d-flex flex-column gap-4">
              <IndexChart />
              <DSEIndex />
              <FetchTopShareBy />
            </div>
            <div
              className="col-lg-6 d-flex flex-column gap-4 wow fadeIn"
              data-wow-delay="0.5s"
            >
              <IndexChartCSE />
              <CSEIndex />
              <FetchTopShareCSEBy />
            </div>
          </div>
        </div>
      </div>
      {/* Chart End */}
      {/* Feature Start */}
      <div className="container-fluid py-5 bg-dark">
        <div className="container py-5">
          <div className="text-center wow fadeIn" data-wow-delay="0.1s">
            <h1 className="mb-5 text-primary bg-light">
              Why Investor{" "}
              <span className="text-uppercase px-2">
                Choose Us
              </span>
            </h1>
          </div>
          <div className="row g-5 align-items-center text-center">
            {features &&
              features.map((item, index) => {
                const delay = (0.1 + index * 0.2).toFixed(1); // 0.1s, 0.3s, 0.5s, etc.
                const icons = [
                  "fa-calendar-alt",
                  "fa-tasks",
                  "fa-pencil-ruler",
                  "fa-user",
                  "fa-hand-holding-usd",
                  "fa-check",
                ];
                return (
                  <div
                    key={index}
                    className="col-md-6 col-lg-4 wow fadeIn text-center"
                    data-wow-delay={`${delay}s`}
                  >
                    <i
                      className={`fa ${icons[index]} fa-4x text-primary mb-3`}
                    ></i>
                    <h4 className="text-white">{item.title}</h4>
                    <p className="mb-0 text-light">{getPlainText(item.description)}</p>
                  </div>
                );
              })}
          </div>
        </div>
      </div>
      {/* Feature End *}
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
