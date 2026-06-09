import { useEffect, useState, useMemo } from "react";
import { useParams } from "react-router-dom";
import Breadcrumbs from "../components/Breadcrumbs";

function ResearchPage() {
  const { id } = useParams();

  const [researchData, setResearchData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    setLoading(true);
    setError(null);

    fetch(`http://127.0.0.1:8000/research/${id}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch research data");
        }
        return res.json();
      })
      .then((data) => {
        setResearchData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  const files = researchData?.files || [];

  const filteredFiles = useMemo(() => {
    if (!query) return files;
    const q = query.toLowerCase();
    return files.filter(
      (f) =>
        (f.title || "").toLowerCase().includes(q) ||
        (f.description || "").toLowerCase().includes(q),
    );
  }, [files, query]);

  return (
    <>
      <Breadcrumbs folder="Research" page={id} />

      <div className="container py-5">
        <div className="text-center mb-4">
          <h1 className="h3 fw-bold">Research Reports</h1>
          <p className="text-muted mb-0">
            Latest market research and company reports — downloadable PDFs.
          </p>
        </div>

        <div className="row align-items-center mb-4">
          <div className="col-md-6 mb-2">
            <div className="input-group shadow-sm">
              <span className="input-group-text bg-white">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  className="bi bi-search"
                  viewBox="0 0 16 16"
                >
                  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85zm-5.242 1.11a5 5 0 1 1 0-10 5 5 0 0 1 0 10z" />
                </svg>
              </span>
              <input
                type="search"
                className="form-control"
                placeholder="Search reports by title or description..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="col-md-6 text-md-end small text-muted">
            {loading ? (
              <span className="me-2">Loading...</span>
            ) : (
              <>
                <strong className="text-dark">{files.length}</strong> total
                reports
                <span className="px-2">•</span>
                <strong className="text-dark">
                  {filteredFiles.length}
                </strong>{" "}
                shown
              </>
            )}
          </div>
        </div>

        {error && (
          <div className="alert alert-danger text-center">⚠️ {error}</div>
        )}

        {loading && (
          <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status"></div>
          </div>
        )}

        {!loading && !error && (
          <div className="mb-5">
            {filteredFiles.length > 0 ? (
              <div className="row g-4">
                {filteredFiles.map((file) => (
                  <div key={file.id} className="col-sm-6 col-md-4">
                    <div className="card h-100 shadow-sm hover-shadow">
                      <div className="card-body d-flex flex-column">
                        <div className="d-flex align-items-start mb-3">
                          <div
                            className="me-3"
                            style={{
                              width: 54,
                              height: 72,
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "center",
                            }}
                          >
                            <svg
                              width="36"
                              height="48"
                              viewBox="0 0 24 24"
                              fill="none"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"
                                fill="#0d6efd"
                              />
                              <path d="M14 2v6h6" fill="#fff" opacity="0.9" />
                            </svg>
                          </div>
                          <div>
                            <h6 className="mb-1 fw-semibold">{file.title}</h6>
                            <div className="text-muted small">
                              {file.description
                                ? file.description.slice(0, 120) +
                                  (file.description.length > 120 ? "..." : "")
                                : "No description"}
                            </div>
                          </div>
                        </div>

                        <div className="mt-auto d-flex justify-content-between align-items-center pt-3 border-top">
                          <div className="small text-secondary">
                            {file.published_at
                              ? new Date(file.published_at).toLocaleDateString()
                              : "—"}
                          </div>

                          <div className="d-flex gap-2">
                            <a
                              href={file.file}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="btn btn-sm btn-outline-primary"
                            >
                              View
                            </a>
                            <a
                              href={file.file}
                              download
                              className="btn btn-sm btn-primary"
                            >
                              Download
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-5">
                <div
                  className="mb-3"
                  style={{ maxWidth: 420, margin: "0 auto" }}
                >
                  <svg
                    width="120"
                    height="80"
                    viewBox="0 0 120 80"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <rect width="120" height="80" rx="8" fill="#f8f9fa" />
                    <path
                      d="M24 52h72"
                      stroke="#dee2e6"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                    <path
                      d="M24 36h72"
                      stroke="#dee2e6"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                    <path
                      d="M36 20h48"
                      stroke="#dee2e6"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
                <h5 className="fw-bold">No reports found</h5>
                <p className="text-muted">
                  Try adjusting your search or check back later for new reports.
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}

export default ResearchPage;
