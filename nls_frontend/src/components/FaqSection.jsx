import { useState, useEffect } from "react";
import { getFaqs } from "../services/getApi";

const FaqSection = () => {
  const [faqs, setFaqs] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadFaqs = async () => {
      try {
        const response = await getFaqs();
        if (response.error) throw new Error(response.error);
        setFaqs(response);
      } catch (err) {
        setError(err.message);
        setFaqs(null);
      }
    };

    loadFaqs();
  }, []);

  if (error) {
    return (
      <div className="container-fluid py-5 bg-dark">
        <div className="container">
          <div className="alert alert-warning text-center">
            Failed to load FAQs: {error}
          </div>
        </div>
      </div>
    );
  }

  if (!faqs || !faqs.length) {
    return null;
  }

  return (
    <div className="container-fluid py-5 bg-dark faq-section">
      <div className="container">
        <div className="text-center wow fadeIn" data-wow-delay="0.1s">
          <h1 className="mb-5 text-primary bg-light">
            Frequently Asked{" "}
            <span className="text-uppercase px-2">Questions</span>
          </h1>
        </div>
        <div className="row justify-content-center">
          <div className="col-lg-8">
            <div className="accordion" id="faq-accordion">
              {faqs.map((item, index) => {
                const headingId = `faq-heading-${index}`;
                const collapseId = `faq-collapse-${index}`;

                return (
                  <div className="accordion-item" key={item.id || index}>
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
                        {item.question}
                      </button>
                    </h2>
                    <div
                      id={collapseId}
                      className={`accordion-collapse collapse ${
                        index === 0 ? "show" : ""
                      }`}
                      aria-labelledby={headingId}
                      data-bs-parent="#faq-accordion"
                    >
                      <div className="accordion-body">{item.answer}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FaqSection;
