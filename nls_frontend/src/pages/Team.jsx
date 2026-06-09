import Breadcrumbs from '../components/Breadcrumbs'
import {useState, useEffect } from "react";
import {getTeams} from "../services/getApi";

function Team(){
    const [teams,setTeams] = useState(null) 
    const [error, setError] = useState(null);

    useEffect(()=>{
        const fetchTeam = async () => {
        try {
            const response = await getTeams(); // Pass the id to API
            setTeams(response);
        } catch (err) {
            setError(err.message);
        }};
        fetchTeam()
    },[])

    if (error) return <p>Error: {error}</p>;
    return (
      <>
        <Breadcrumbs folder="Pages" page="Board Members" />
        {/* Team Start */}
        <div className="container-fluid bg-light py-5">
          <div className="container py-5">
            <h1 className="mb-5">
              Our Board of {" "}
              <span className="text-uppercase text-primary bg-light px-2">
                Directors
              </span>
            </h1>
            <div className="row g-4">
              {teams ? (
                teams.map((member, index) => (
                  <div
                    key={index}
                    className="col-md-6 col-lg-3 wow fadeIn"
                    data-wow-delay="0.1s"
                  >
                    <div className="team-item position-relative overflow-hidden">
                      <img
                        className="img-fluid w-100"
                        src={
                          member.image
                            ? "http://127.0.0.1:8000" + member.image
                            : "No team-1 image"
                        }
                        alt=""
                      />
                      <div className="team-overlay">
                        <small className="mb-2">{member.designation}</small>
                        <h4 className="lh-base text-light">{member.name}</h4>
                        {/* <div className="d-flex justify-content-center">
                         
                        </div> */}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center p-5">
                  <div
                    className="spinner-border text-primary mb-3"
                    role="status"
                  ></div>
                  <p className="text-muted">
                    Loading db data or backend unavailable...
                  </p>
                </div>
              )}

              {/* <div className="col-md-6 col-lg-3 wow fadeIn" data-wow-delay="0.3s">
                        <div className="team-item position-relative overflow-hidden">
                            <img className="img-fluid w-100" src="assets/img/team-2.jpg" alt=""/>
                            <div className="team-overlay">
                                <small className="mb-2">Architect</small>
                                <h4 className="lh-base text-light">Donald Pakura</h4>
                                <div className="d-flex justify-content-center">
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-facebook-f"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-twitter"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-instagram"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-linkedin-in"></i>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-6 col-lg-3 wow fadeIn" data-wow-delay="0.5s">
                        <div className="team-item position-relative overflow-hidden">
                            <img className="img-fluid w-100" src="assets/img/team-3.jpg" alt=""/>
                            <div className="team-overlay">
                                <small className="mb-2">Architect</small>
                                <h4 className="lh-base text-light">Bradley Gordon</h4>
                                <div className="d-flex justify-content-center">
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-facebook-f"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-twitter"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-instagram"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-linkedin-in"></i>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-6 col-lg-3 wow fadeIn" data-wow-delay="0.7s">
                        <div className="team-item position-relative overflow-hidden">
                            <img className="img-fluid w-100" src="assets/img/team-4.jpg" alt=""/>
                            <div className="team-overlay">
                                <small className="mb-2">Architect</small>
                                <h4 className="lh-base text-light">Alexander Bell</h4>
                                <div className="d-flex justify-content-center">
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-facebook-f"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-twitter"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-instagram"></i>
                                    </Link>
                                    <Link className="btn btn-outline-primary btn-sm-square border-2 me-2" href="#!">
                                        <i className="fab fa-linkedin-in"></i>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div> */}
            </div>
          </div>
        </div>
        {/* Team End */}
      </>
    );
}
export default Team