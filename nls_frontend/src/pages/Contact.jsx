import Breadcrumbs from '../components/Breadcrumbs'
function Contact(){

    return(
        <>
        <Breadcrumbs folder="Pages" page="Contact"/>
        {/*<!-- Contact Start -->*/}
        <div className="container-fluid py-5">
            <div className="container py-5">
                <div className="text-center wow fadeIn" data-wow-delay="0.1s">
                    <h1 className="mb-5">Have Any Query? <span className="text-uppercase text-primary bg-light px-2">Contact
                            Us</span></h1>
                </div>
                <div className="row justify-content-center">
                    <div className="col-lg-7">
                        <p className="text-center mb-4">The contact form is currently inactive. Get a functional and working
                            contact form with Ajax & PHP in a few minutes. Just copy and paste the files, add a little code
                            and you're done. <a href="https://htmlcodex.com/contact-form">Download Now</a>.</p>
                        <div className="wow fadeIn" data-wow-delay="0.3s">
                            <form>
                                <div className="row g-3">
                                    <div className="col-md-6">
                                        <div className="form-floating">
                                            <input type="text" className="form-control" id="name" placeholder="Your Name"/>
                                            <label for="name">Your Name</label>
                                        </div>
                                    </div>
                                    <div className="col-md-6">
                                        <div className="form-floating">
                                            <input type="email" className="form-control" id="email" placeholder="Your Email"/>
                                            <label for="email">Your Email</label>
                                        </div>
                                    </div>
                                    <div className="col-12">
                                        <div className="form-floating">
                                            <input type="text" className="form-control" id="subject" placeholder="Subject"/>
                                            <label for="subject">Subject</label>
                                        </div>
                                    </div>
                                    <div className="col-12">
                                        <div className="form-floating">
                                            <textarea className="form-control" placeholder="Leave a message here" id="message"
                                                style={{height: "150px"}}></textarea>
                                            <label for="message">Message</label>
                                        </div>
                                    </div>
                                    <div className="col-12">
                                        <button className="btn btn-primary w-100 py-3" type="submit">Send Message</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {/*<!-- Contact End -->*/}
        </>
    )
}

export default Contact