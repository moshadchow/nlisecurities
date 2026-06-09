import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import ContentPage from "../components/ContentPage";
import { getServices } from "../services/getApi";
import { Link } from "react-router-dom";


const ServiceDetails = ()=>{
  const { id } = useParams();
  const [html, setHtml] = useState("");
  const [services, setServices] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(()=>{
        const fetchAllService = async (id) => {
        try {
            setLoading(true);
            const response = await getServices(id); // Pass the id to API
            setServices(response);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
        };
        fetchAllService(null)
    },[])

  useEffect(() => {
    const fetchService = async () => {
      try {
        setLoading(true);
        const response = await getServices(id) // Pass the id to API
        setHtml(response);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchService();
  }, [id]); // Re-run when id changes

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
     <div className="container-fluid py-5">
      <div className="row">
        {/* Sidebar */}
        <div className="col-md-3 mb-4">
          <div className="list-group shadow-sm">
            <h5 className="list-group-item active bg-primary border-0">services</h5>
            {services && services.length > 0 ? (
              services.map((service) => (
                <Link
                  key={service.id}
                  to={`/service_dtl/${service.id}`}
                  className={`list-group-item list-group-item-action ${
                    Number(id) === service.id ? "active" : ""
                  }`}
                >
                  {service.title}
                </Link>
              ))
            ) : (
              <div className="list-group-item text-muted">No services found</div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="col-md-9">
          <ContentPage html={html} />
        </div>
      </div>
    </div>
  );
}

export default ServiceDetails;