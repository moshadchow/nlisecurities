import "../assets/ckeditor-styles.css";
import DOMPurify from "dompurify";

const MEDIA_URL = "http://127.0.0.1:8000/"; // note the trailing slash

const CKEditorViewer = ({ html }) => {
  const addMediaPrefixToImageSrc = (inputHtml) => {
    if (!inputHtml) return "";

    const div = document.createElement("div");
    div.innerHTML = inputHtml;

    const images = div.querySelectorAll("img");

    images.forEach((img) => {
      const src = img.getAttribute("src");
      if (!src) return;

      // Skip absolute URLs and base64
      if (src.startsWith("http") || src.startsWith("data:")) return;

      // Normalize: ensure the path starts with a single leading slash
      const normalizedSrc = src.startsWith("/") ? src : `/${src}`;

      // Normalize MEDIA_URL: remove trailing slash, then add normalizedSrc
      const base = MEDIA_URL.replace(/\/$/, "");
      img.setAttribute("src", `${base}${normalizedSrc}`);
    });

    return div.innerHTML;
  };

  const processedHtml = addMediaPrefixToImageSrc(html);
  const cleanHtml = DOMPurify.sanitize(processedHtml);

  return (
    <div
      className="ckeditor-content"
      dangerouslySetInnerHTML={{ __html: cleanHtml }}
    />
  );
};

export default CKEditorViewer;
