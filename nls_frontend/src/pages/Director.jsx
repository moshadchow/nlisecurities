import Breadcrumbs from '../components/Breadcrumbs'
import { useState, useEffect } from "react";
import {getBoardMembers} from "../services/getApi";

function Director() {
  const [directors, setDirectors] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBoardMembers = async (id) => {
      try {
        const response = await getBoardMembers(id);
        setDirectors(response);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchBoardMembers(null);
  }, []);

  if (error) return <p>Error: {error}</p>;

  return (
    <>
      <Breadcrumbs folder="Pages" page="Board Members" />

      <div className="container-fluid bg-light py-5">
        <div className="container py-5">
          <h1 className="mb-5">
            Our Board of{" "}
            <span className="text-uppercase text-primary bg-light px-2">
              Directors
            </span>
          </h1>

          <div className="row g-4">
            {directors.length > 0 ? (
              directors.map((member, index) => (
                <div key={index} className="col-md-6 col-lg-3">
                  <div className="team-item position-relative overflow-hidden">
                    <img
                      className="img-fluid w-100"
                      src={
                        member.image
                          ? `http://127.0.0.1:8000${member.image}`
                          : "/placeholder.jpg"
                      }
                      alt={member.name}
                    />
                    <div className="team-overlay">
                      <small className="mb-2">{member.designation}</small>
                      <h4 className="lh-base text-light">{member.name}</h4>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center p-5 w-100">
                <div className="spinner-border text-primary mb-3" />
                <p className="text-muted">
                  Loading db data or backend unavailable...
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default Director;
