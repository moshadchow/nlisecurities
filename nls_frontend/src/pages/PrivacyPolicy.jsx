import Breadcrumbs from '../components/Breadcrumbs'
import { useState, useEffect } from "react";
import ContentPage from "../components/ContentPage";
import { getPolicy } from '../services/getApi';

const PrivacyPolicy = () =>{
    const [html, setHtml] = useState("");
    const [loading, setLoading] = useState(false); 
    const [error, setError] = useState(null); 

    useEffect(() => {
        const fetchPolicy = async () => {
          try {
            setLoading(true);
            const response = await getPolicy() // Pass the id to API
            setHtml(response);
          } catch (err) {
            setError(err.message);
          } finally {
            setLoading(false);
          }
        }
        fetchPolicy();
      }, []); // Re-run when id changes
    
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error: {error}</p>;
      return (
        <>
          <Breadcrumbs folder="Pages" page="Privacy Policy" />
          <ContentPage html={html} />
        </>
      );
}

export default PrivacyPolicy;
