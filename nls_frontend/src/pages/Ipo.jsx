import Breadcrumbs from '../components/Breadcrumbs'
import {useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getIPO } from '../services/getApi';
function Ipo(){
    const [ipo,setIpo] = useState(null) 
    const [error, setError] = useState(null);

    useEffect(()=>{
        let interval;
        const fetchIPOOffer = async () => {
        try {
            const response = await getIPO(); // Pass the id to API
            setIpo(response);
        } catch (err) {
            setError(err.message);
        } 
        };
        fetchIPOOffer()
        // Set interval to refresh every 10 seconds
        interval = setInterval(() => {
                    fetchIPOOffer();
        }, 10000); // 10,000 ms = 10 sec
        // Cleanup interval on component unmount
        return () => clearInterval(interval);
    },[])
return (
  <>
    <Breadcrumbs folder="Pages" page="ForthComming IPO" />
    <div className="container-fluid py-5">
      <div className="container">
        <table className="table table-success table-striped">
          <thead>
            <tr>
              <th>Sl#</th>
              <th>Compnay</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {ipo ? (
              ipo.map((item, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{item.company}</td>
                  <td>
                    <Link
                      to={`https://www.dsebd.org/${item.href.replace(
                        "/media",
                        ""
                      )}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      IPO Details
                    </Link>
                  </td>
                </tr>
              ))
            ) : (
              <div className="text-center p-5">
                <div
                  className="spinner-border text-primary mb-3"
                  role="status"
                ></div>
                <p className="text-muted">
                  Loading market data or backend unavailable...
                </p>
              </div>
            )}
          </tbody>
        </table>
      </div>
    </div>
  </>
);
}
export default Ipo