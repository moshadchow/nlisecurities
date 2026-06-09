import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import ContentPage from "./ContentPage";
import { getEvents } from "../services/getApi";
import { Link } from "react-router-dom";


const EventDetails = ()=>{
  const { id } = useParams();
  const [html, setHtml] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllEvents = async (id) => {
      try {
        const response = await getEvents(id); // all events
        setEvents(response);
      } catch (err) {
        console.error("Failed to load events", err);
      }
    };
    fetchAllEvents(null);
  }, []);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        setLoading(true);
        const response = await getEvents(id) // Pass the id to API
        setHtml(response);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchEvent();
  }, [id]); // Re-run when id changes

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="container-fluid py-5">
      <div className="row">
        {/* Sidebar */}
        <div className="col-md-3 mb-4">
          <div className="list-group shadow-sm">
            <h5 className="list-group-item active bg-primary border-0">Events</h5>
            {events && events.length > 0 ? (
              events.map((event) => (
                <Link
                  key={event.id}
                  to={`/event_dtl/${event.id}`}
                  className={`list-group-item list-group-item-action ${
                    Number(id) === event.id ? "active" : ""
                  }`}
                >
                  {event.title}
                </Link>
              ))
            ) : (
              <div className="list-group-item text-muted">No events found</div>
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

export default EventDetails;