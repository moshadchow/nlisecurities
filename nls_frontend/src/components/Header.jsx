import { Link } from "react-router-dom";
import { fetchMarketInfo } from "../services/chartService";
import { useState, useEffect } from "react";
import Ticker from "../components/Ticker";

function Header() {
  const [indexData, setIndexData] = useState(null);
  const [indexDataCSE, setIndexDataCSE] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
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

    loadMarketIndex();
    const interval = setInterval(loadMarketIndex, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      {/* ===== TICKER START ===== */}
      <div
        className="container-fluid text-light py-1"
        style={{ backgroundColor: "#003d7a" }}
      >
        <Ticker />
      </div>
      {/* ===== TICKER END ===== */}

      {/* ===== TOP BAR START ===== */}
      <div
        className="container-fluid text-light py-2"
        style={{ backgroundColor: "#003d7a" }}
      >
        <div className="container">
          <div className="row align-items-center">
            {/* Address & Phone */}
            <div className="col-lg-6 text-center text-lg-start small">
              <i className="bi bi-geo-alt me-2 fs-4"></i>
              79 Motijheel C/A, Dhaka-1000
              <span className="mx-3">|</span>
              <i className="bi bi-telephone me-2 fs-4"></i>
              +88 09678771266
            </div>

            {/* Social + Trade Button */}
            <div className="col-lg-6 text-center text-lg-end mt-2 mt-lg-0">
              <a
                href="https://www.facebook.com/nlisecurities"
                target="_blank"
                rel="noopener noreferrer"
                className="text-light me-3 fs-4"
              >
                <i className="bi bi-facebook"></i>
              </a>

              <a
                href="https://www.linkedin.com/company/nli-securities-limited/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-light me-3 fs-4"
              >
                <i className="bi bi-linkedin"></i>
              </a>

              <Link
                to="https://nls.xfltrade.com"
                target="_blank"
                className="btn btn-danger btn-sm ms-2"
              >
                Trade Now
              </Link>
            </div>
          </div>
        </div>
      </div>
      {/* ===== TOP BAR END ===== */}

      {/* ===== NAVBAR START ===== */}
      <div className="container-fluid sticky-top bg-light shadow-sm">
        <div className="container">
          <nav className="navbar navbar-expand-lg navbar-light py-3">
            <Link to="/" className="navbar-brand me-5">
              <img
                src="http://127.0.0.1:8000/media/nls_logo.png"
                alt="NLI Securities"
                style={{ height: "60px", objectFit: "contain" }}
              />
            </Link>

            <button
              className="navbar-toggler ms-auto"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarCollapse"
            >
              <span className="navbar-toggler-icon"></span>
            </button>

            <div className="collapse navbar-collapse" id="navbarCollapse">
              <div className="navbar-nav ms-auto fw-semibold">
                <Link to="/" className="nav-link site-nav-link active">
                  Home
                </Link>

                <Link to="/about" className="nav-link site-nav-link">
                  About
                </Link>

                <Link to="/service" className="nav-link site-nav-link">
                  Services
                </Link>

                <Link to="/branch" className="nav-link site-nav-link">
                  Branch
                </Link>

                {/* Research Dropdown */}
                <div className="nav-item dropdown">
                  <Link
                    to="#!"
                    className="nav-link dropdown-toggle site-nav-link"
                    data-bs-toggle="dropdown"
                  >
                    Research
                  </Link>
                  <div className="dropdown-menu">
                    <Link
                      to="/research/DailyNewsFlash"
                      className="dropdown-item"
                    >
                      Daily News Flash
                    </Link>
                    <Link
                      to="/research/DailyMarketUpdate"
                      className="dropdown-item"
                    >
                      Daily Market Update
                    </Link>
                    <Link
                      to="/research/WeeklyMarketReview"
                      className="dropdown-item"
                    >
                      Weekly Market Review
                    </Link>
                    <Link
                      to="/research/WeeklyMutualFundReport"
                      className="dropdown-item"
                    >
                      Weekly Mutual Fund Report
                    </Link>
                    <Link
                      to="/research/EquitySnapshot"
                      className="dropdown-item"
                    >
                      Equity Snapshot
                    </Link>
                    <Link to="/research/IPOInsights" className="dropdown-item">
                      IPO Insights
                    </Link>
                    <Link
                      to="/research/EarningUpdates"
                      className="dropdown-item"
                    >
                      Earning Updates
                    </Link>
                    <Link to="/research/MacroReport" className="dropdown-item">
                      Macro Report
                    </Link>
                    <Link to="/research/SectorReport" className="dropdown-item">
                      Sector Report
                    </Link>
                  </div>
                </div>
                {/* Market Dropdown */}
                <div className="nav-item dropdown">
                  <Link
                    to="#!"
                    className="nav-link dropdown-toggle site-nav-link"
                    data-bs-toggle="dropdown"
                  >
                    Market
                  </Link>
                  <div className="dropdown-menu">
                    <Link to="/marketNews" className="dropdown-item">
                      News
                    </Link>
                    <Link to="/sector" className="dropdown-item">
                      Sector Info
                    </Link>
                  </div>
                </div>
                {/* Information Dropdown */}
                <div className="nav-item dropdown">
                  <Link
                    to="#!"
                    className="nav-link dropdown-toggle site-nav-link"
                    data-bs-toggle="dropdown"
                  >
                    Information
                  </Link>
                  <div className="dropdown-menu">
                    <Link to="/director" className="dropdown-item">
                      Board of Directors
                    </Link>
                    <Link to="/ipo" className="dropdown-item">
                      Forthcoming IPO
                    </Link>
                    <Link to="/download" className="dropdown-item">
                      Download
                    </Link>
                    <Link to="/privacy-policy" className="dropdown-item">
                      Privacy Policy
                    </Link>
                  </div>
                </div>

                <Link to="/contact" className="nav-link site-nav-link">
                  Contact
                </Link>
                {/* Client Portal */}
                <a
                  href="https://clientportal.nlisecurities.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline-primary btn-sm ms-4"
                >
                  <i className="bi bi-person-circle me-1"></i>
                  Investor Portal
                </a>
              </div>
            </div>
          </nav>
        </div>
      </div>
      {/* ===== NAVBAR END ===== */}
    </>
  );
}

export default Header;