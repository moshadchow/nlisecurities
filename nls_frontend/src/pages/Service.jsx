import Breadcrumbs from '../components/Breadcrumbs';
import { useState, useEffect } from "react";
import { getPlainText, getServices } from "../services/getApi";
import { Link } from "react-router-dom";

const Service = () => {
  const [services, setServices] = useState([]);      // start with empty array
  const [loading, setLoading] = useState(true);      // loading is true initially
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchService = async (id) => {
      try {
        setLoading(true);
        const response = await getServices(id);        // no need for id here
        setServices(response || []);
      } catch (err) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

    fetchService(null);
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <>
      <Breadcrumbs folder="Pages" page="Services" />
      {/* Service Start */}
      <div className="container-fluid py-5">
        <div className="container py-5">
          <div className="row g-5 align-items-center">
            <div className="col-lg-5 wow fadeIn" data-wow-delay="0.1s">
              <h1 className="mb-5">
                Our Dedicated{" "}
                <span className="text-uppercase text-primary bg-light px-2">
                  Services
                </span>
              </h1>
              <p>
                NLI Securities acts as the bridge between investors and the
                stock market. Its core role is to help clients buy and sell
                securities, manage their accounts, ensure smooth settlement of
                trades, and provide guidance for informed investment
                decisions.
              </p>
              <p className="mb-5">
                In essence, we make market participation possible, safe, and
                efficient for individual and institutional investors.
              </p>
              <div className="d-flex align-items-center bg-light">
                <div
                  className="btn-square flex-shrink-0 bg-primary"
                  style={{ width: "100px", height: "100px" }}
                >
                  <i className="fa fa-phone fa-2x text-white"></i>
                </div>
                <div className="px-3">
                  <h3>+88 02 57165253</h3>
                  <span>Call us direct 24/7 for get a free consultation</span>
                </div>
              </div>
            </div>

            <div className="col-lg-7">
              <div className="row g-0">
                {services.length > 0 ? (
                  services.map((item, index) => {
                    const delay = 0.2 + index * 0.2;

                    const fullText = item.description
                      ? getPlainText(item.description)
                      : "No service description";

                    const shortText =
                      fullText.length > 150
                        ? fullText.substring(0, 150) + "..."
                        : fullText;

                    return (
                      <div
                        key={item.id || index}
                        className="col-md-6 wow fadeIn"
                        data-wow-delay={`${delay}s`}
                      >
                        <div className="service-item h-100 d-flex flex-column justify-content-center bg-primary p-3 rounded">
                          <Link
                            to={`/service_dtl/${item.id}`}
                            className="service-img position-relative mb-3"
                          >
                            <img
                              className="img-fluid w-100"
                              src={
                                item.image
                                  ? "http://127.0.0.1:8000" + item.image
                                  : "/placeholder-service.jpg"
                              }
                              alt={item.title || "Service image"}
                              style={{
                                height: "250px",
                                objectFit: "cover",
                                borderRadius: "8px",
                              }}
                            />
                            <h3 className="mt-2 mb-0 text-white">
                              {item.title}
                            </h3>
                          </Link>

                          {/* Clamp text so it doesn't overflow the card */}
                          <p
                            className="mb-0 text-light"
                            style={{
                              display: "-webkit-box",
                              WebkitLineClamp: 4,          // max 4 lines
                              WebkitBoxOrient: "vertical",
                              overflow: "hidden",
                              wordWrap: "break-word",
                            }}
                          >
                            {shortText}
                          </p>
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <div className="text-center p-5">
                    <div
                      className="spinner-border text-primary mb-3"
                      role="status"
                    ></div>
                    <p className="text-muted mb-0">No services available.</p>
                  </div>
                )}
              </div>
            </div>

          </div>
        </div>
      </div>
      {/* Service End */}
    </>
  );
};

export default Service;
