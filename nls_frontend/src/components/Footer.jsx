import { Link } from 'react-router-dom'

function Footer() {
  return (
    <>
      {/* Footer Start */}
      <div className="container-fluid bg-dark text-white-50 footer pt-5">
        <div className="container py-5">
          <div className="row g-5">
            <div
              className="col-md-6 col-lg-3 wow fadeIn"
              data-wow-delay="0.1s"
            >
              <Link to="/" className="d-inline-block mb-3">
                <img
                  src="http://127.0.0.1:8000/media/nls_logo.png"
                  alt="NLI Securities"
                  style={{ height: "70px", objectFit: "contain" }}
                />
              </Link>
              <p className="mb-0">
                Founded in 2013, NLI Securities Limited (NLS) is a
                full-fledged corporate member of both the Dhaka Stock Exchange
                (DSE) and the Chittagong Stock Exchange (CSE).
              </p>
            </div>
            <div
              className="col-md-6 col-lg-3 wow fadeIn"
              data-wow-delay="0.3s"
            >
              <h5 className="text-white mb-4">Get In Touch</h5>
              <p>
                <i className="fa fa-map-marker-alt me-3"></i>NLI Tower (1st
                Floor), South Side, 54 Kazi Nazrul Islam Avenue, Kawran Bazar,
                Dhaka-1215
              </p>
              <p>
                <i className="fa fa-phone-alt me-3"></i> +88 02 57165253
              </p>
              <p>
                <i className="fa fa-envelope me-3"></i>
                nlisecurities244@gmail.com
              </p>
              <div className="d-flex pt-2">
                <Link
                  className="btn btn-outline-primary btn-square border-2 me-2"
                  href="#!"
                >
                  <i className="fab fa-twitter"></i>
                </Link>
                <Link
                  className="btn btn-outline-primary btn-square border-2 me-2"
                  href="#!"
                >
                  <i className="fab fa-facebook-f"></i>
                </Link>
                <Link
                  className="btn btn-outline-primary btn-square border-2 me-2"
                  href="#!"
                >
                  <i className="fab fa-youtube"></i>
                </Link>
                <Link
                  className="btn btn-outline-primary btn-square border-2 me-2"
                  href="#!"
                >
                  <i className="fab fa-instagram"></i>
                </Link>
                <Link
                  className="btn btn-outline-primary btn-square border-2 me-2"
                  href="#!"
                >
                  <i className="fab fa-linkedin-in"></i>
                </Link>
              </div>
            </div>
            <div
              className="col-md-6 col-lg-3 wow fadeIn"
              data-wow-delay="0.5s"
            >
              <h5 className="text-white mb-4">Popular Link</h5>
              <Link className="btn btn-link" to="/about">
                About Us
              </Link>
              <Link className="btn btn-link" to="/contact">
                Contact Us
              </Link>
              <Link className="btn btn-link" to="/privacy-policy">
                Privacy Policy
              </Link>
              <Link className="btn btn-link" to="/download">
                Download
              </Link>
              <Link className="btn btn-link" to="/career">
                Career
              </Link>
            </div>
            <div
              className="col-md-6 col-lg-3 wow fadeIn"
              data-wow-delay="0.7s"
            >
              <h5 className="text-white mb-4">Our Services</h5>
              <Link className="btn btn-link" href="#!">
                Brokerage Service
              </Link>
              <Link className="btn btn-link" href="#!">
                DP Service
              </Link>
              <Link className="btn btn-link" href="#!">
                Margin Service
              </Link>
              <Link className="btn btn-link" href="#!">
                Advisory Service
              </Link>
              <Link className="btn btn-link" href="#!">
                Trade Execution
              </Link>
            </div>
          </div>
        </div>
        <div className="container wow fadeIn" data-wow-delay="0.1s">
          <div className="copyright">
            <div className="row">
              <div className="col-md-6 text-center text-md-start mb-3 mb-md-0">
                &copy;{" "}
                <Link className="border-bottom" href="#!">
                  NLI Securities
                </Link>
                , All Right Reserved,
                {/* This template is free as long as you keep the below author’s credit link/attribution link/backlink. */}
                {/* If you'd like to use the template without the below author’s credit link/attribution link/backlink, */}
                {/* you can purchase the Credit Removal License from "https://htmlcodex.com/credit-removal". */}
                Designed By{" "}
                <Link
                  className="border-bottom"
                  href="https://xpertfintech.com"
                >
                  Xpert Fintech Ltd.
                </Link>
              </div>
              <div className="col-md-6 text-center text-md-end">
                <div className="footer-menu">
                  <Link to="#!">Home</Link>
                  <Link to="#!">Cookies</Link>
                  <Link to="#!">Help</Link>
                  <Link to="#!">FAQs</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Footer End */}
    </>
  );
}
export default Footer