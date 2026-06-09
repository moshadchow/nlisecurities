import { useState } from "react";

import BranchContainer from '../components/BranchContainer';
const Branch = () =>{
    const [category,setCategory] = useState([])
    return (
      <>
        <div className="container-fluid py-5">
          <div className="container">
            <nav className="navbar navbar-light bg-light">
              <form className="container-fluid justify-content-start">
                <button
                  className="btn btn-outline-success me-2"
                  type="button"
                  onClick={(e) => {
                    e.preventDefault(); // stops page reload
                    setCategory("branch");
                  }}
                >
                  Branch
                </button>
                <button
                  className="btn btn-outline-success me-2"
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    setCategory("extension");
                  }}
                >
                  Extension
                </button>
                <button
                  className="btn btn-outline-success me-2"
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    setCategory("booth");
                  }}
                >
                  Booth
                </button>
              </form>
            </nav>
            <br />
            {/* Pass selected category */}
            <BranchContainer category={category} />
          </div>
        </div>
      </>
    );
}

export default Branch