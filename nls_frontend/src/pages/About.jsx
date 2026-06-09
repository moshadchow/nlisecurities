import Breadcrumbs from '../components/Breadcrumbs'
import {useState, useEffect } from "react";
import ContentPage from "../components/ContentPage";
import {getAbout} from "../services/getApi";
import TeamSection from "../components/TeamSection";
import { Link } from "react-router-dom";

function About(){
     const [about,setAbout] = useState(null) 
     const [loading,setLoading] = useState(false) 
     const [error, setError] = useState(null);
     useEffect(()=>{
        const fetchAbout = async () => {
        try {
            setLoading(true);
            const response = await getAbout(); // Pass the id to API
            setAbout(response);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
        };
        fetchAbout()
    },[])
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    return (
      <>
        <Breadcrumbs folder="Pages" page="About" />

        {/* About Start */}
        <div className="container-fluid py-5">
          <div className="container">
            <div className="row g-5">
              {/* RIGHT: CONTENT */}
              <div className="col-lg-12 wow fadeIn" data-wow-delay="0.5s">
                <ContentPage html={about} />

                <div className="row g-3 mt-4">
                  <div className="col-sm-6">
                    <h6 className="mb-3">
                      <i className="fa fa-check text-primary me-2"></i>
                      Trusted Market Expertise
                    </h6>
                    <h6 className="mb-0">
                      <i className="fa fa-check text-primary me-2"></i>
                      Dedicated Professional Team
                    </h6>
                  </div>
                  <div className="col-sm-6">
                    <h6 className="mb-3">
                      <i className="fa fa-check text-primary me-2"></i>
                      Reliable Customer Support
                    </h6>
                    <h6 className="mb-0">
                      <i className="fa fa-check text-primary me-2"></i>
                      Competitive Brokerage Rates
                    </h6>
                  </div>
                </div>

                <div className="d-flex align-items-center mt-5">
                  <Link className="btn btn-primary px-4 me-2">Read More</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* About End */}

        {/* ✅ Team Section — full width */}
        <TeamSection />
      </>
    );
}
export default About