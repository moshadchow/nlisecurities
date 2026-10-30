const FeatureCard = ({ title, description, iconClass }) => (
  <div className="feature-card">
    <div className="feature-card-icon">
      <i className={`fa ${iconClass} fa-2x`} aria-hidden="true" />
    </div>
    <h3 className="feature-card-title">{title}</h3>
    <div
      className="feature-card-description"
      dangerouslySetInnerHTML={{ __html: description }}
    />
  </div>
);

export default FeatureCard;
