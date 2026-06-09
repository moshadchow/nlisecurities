import CKEditorViewer from "./CKEditorViewer"; // your viewer component

const ContentPage = ({ html }) => {
  return (
    <>
      <section className="py-5 bg-light">
        <div className="container">
          <div
            className="text-center mb-5"
            data-wow-delay="0.2s"
            style={{ maxWidth: "800px", margin: "0 auto" }}
          >
            <h2 className="fw-bold text-primary mb-3">
              {html?.title || "Content Title"}
            </h2>
            {/* <p className="text-muted">
              {html?.subtitle || "Here’s a detailed article or content section."}
            </p> */}
          </div>

          <div className="card border-0 shadow-sm p-4">
            <div className="card-body">
              {html ? (
                <CKEditorViewer html={html.description} />
              ) : (
                <div className="text-center text-muted py-5">
                  Loading content...
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default ContentPage;
