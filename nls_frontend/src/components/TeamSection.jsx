import { useEffect, useState } from "react";
import { getTeams } from "../services/getApi";

const TeamSection = () => {
  const [teams, setTeams] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        const response = await getTeams();
        setTeams(response);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchTeam();
  }, []);

  if (error) return <p>Error: {error}</p>;

  return (
    <div className="container-fluid bg-light py-5 mt-5">
      <div className="container py-5">
        <h1 className="mb-5">
          Our Professional{" "}
          <span className="text-uppercase text-primary bg-light px-2">
            Team
          </span>
        </h1>

        <div className="row g-4">
          {teams ? (
            teams.map((member, index) => (
              <div
                key={member.id || index}
                className="col-md-6 col-lg-3 wow fadeIn"
                data-wow-delay="0.1s"
              >
                <div className="team-item position-relative overflow-hidden">
                  <img
                    className="img-fluid w-100"
                    src={
                      member.image
                        ? "http://127.0.0.1:8000" + member.image
                        : "No Image"
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
            <div className="text-center p-5">
              <div className="spinner-border text-primary mb-3" />
              <p className="text-muted">Loading team...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TeamSection;
