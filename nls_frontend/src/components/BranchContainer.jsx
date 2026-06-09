import { useEffect, useState } from "react";
import { getBranches } from "../services/getApi";

const BranchContainer = ({ category }) => {
  const [branches, setBranches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openMapIndex, setOpenMapIndex] = useState(null);

  useEffect(() => {
    if (!category) {
      setBranches([]);
      setLoading(false);
      return;
    }

    const fetchBranches = async () => {
      try {
        setLoading(true);
        const data = await getBranches(category);
        setBranches(data || []);
      } catch (err) {
        console.error("Error fetching branches:", err);
        setBranches([]);
      } finally {
        setLoading(false);
      }
    };

    fetchBranches(category);
  }, [category]);

  if (loading) return <div className="text-center py-5 text-muted">Loading...</div>;
  if (!branches.length) return <div className="text-center py-5 text-muted">No branches found.</div>;

  return (
    <div className="overflow-x-auto">
      <table className="table table-bordered border-primary w-full text-sm">
        <thead>
          <tr>
            <th>#</th>
            <th>Office</th>
            <th>Address</th>
            <th>Email</th>
            <th>Contact</th>
            <th>Location</th>
          </tr>
        </thead>

        <tbody>
          {branches.map((item, index) => (
            <>
              <tr key={item.id || index}>
                <td>{index + 1}</td>
                <td>{item.office}</td>
                <td>{item.address}</td>
                <td>{item.email}</td>
                <td>{item.contact}</td>
                <td>
                  {item.lat && item.lng ? (
                    <button
                      className="btn btn-sm btn-outline-primary"
                      onClick={() =>
                        setOpenMapIndex(openMapIndex === index ? null : index)
                      }
                    >
                      {openMapIndex === index ? "Hide Map" : "View Map"}
                    </button>
                  ) : (
                    <span className="text-muted">N/A</span>
                  )}
                </td>
              </tr>

              {openMapIndex === index && item.lat && item.lng && (
                <tr>
                  <td colSpan="6">
                    <div className="ratio ratio-16x9">
                      <iframe
                        src={`https://www.google.com/maps?q=${item.lat},${item.lng}&z=16&output=embed`}
                        loading="lazy"
                        referrerPolicy="no-referrer-when-downgrade"
                        title={`Map - ${item.office}`}
                      />
                    </div>
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BranchContainer;
