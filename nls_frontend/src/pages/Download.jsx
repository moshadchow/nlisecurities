import { useEffect, useState } from "react";
import { getFilesByCategories } from "../services/getApi";
import Breadcrumbs from '../components/Breadcrumbs'

const Download = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await getFilesByCategories()
        setCategories(res);
      } catch (err) {
        console.error("Error fetching categories:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  if (loading) return <p className="text-center mt-5">Loading...</p>;

  return (
    <>
    <Breadcrumbs folder="Market" page="Download" />
    <div className="container mt-4">
      {/* <h2 className="text-center mb-4">Download Center</h2> */}
      {categories.length === 0 && <p>No files available.</p>}

      {categories.map((cat) => (
        <div key={cat.id} className="mb-5">
          <h4 className="mb-3 border-bottom pb-2">{cat.name}</h4>

          {cat.files && cat.files.length > 0 ? (
            <ul className="list-group">
              {cat.files.map((file) => (
                <li
                  key={file.id}
                  className="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    <strong>{file.title}</strong>
                    {file.description && (
                      <p className="mb-0 text-muted small">
                        {file.description}
                      </p>
                    )}
                  </div>
                  <a
                    href={`http://127.0.0.1:8000/${file.file}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-sm btn-primary"
                  >
                    Download
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-muted">No files found in this category.</p>
          )}
        </div>
      ))}
    </div>
    </>
  );
};

export default Download;
