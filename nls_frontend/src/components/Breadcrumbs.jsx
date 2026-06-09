import { Link } from 'react-router-dom'
function Breadcrumbs(props) {
    return (
        <>
            {/* Hero Start */}
            <div className="container-fluid bg-primary hero-header" style={{ paddingTop: "120px", paddingBottom: "40px" }}>
                <div className="container">
                    {/* Page Heading - centered and prominent */}
                    <div className="text-center mb-4 animated slideInLeft">
                        <h1 className="display-2 fw-bold text-blue mb-2">{props.page}</h1>
                    </div>

                    {/* Breadcrumb Navigation - centered below heading */}
                    <div className="row justify-content-center animated slideInRight">
                        <div className="col-auto">
                            <nav aria-label="breadcrumb">
                                <ol className="breadcrumb mb-0 bg-transparent">
                                    <li className="breadcrumb-item">
                                        <Link className="text-blue text-decoration-none" to="/">Home</Link>
                                    </li>
                                    {props.folder && (
                                        <li className="breadcrumb-item">
                                            <Link className="text-blue text-decoration-none" to="#">{props.folder}</Link>
                                        </li>
                                    )}
                                    <li className="breadcrumb-item text-blue-50 active" aria-current="page">
                                        {props.page}
                                    </li>
                                </ol>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
            {/* Hero End */}
        </>
    )
}

export default Breadcrumbs