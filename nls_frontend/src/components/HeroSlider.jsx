import { useState, useEffect } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { getCarousal } from "../services/getApi";

const HeroSlider = () => {
  const [sliders, setSliders] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCarousal = async () => {
      try {
        const response = await getCarousal();
        setSliders(response);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchCarousal();
  }, []);

  const settings = {
    dots: true,
    infinite: true,
    speed: 700,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3500,
    fade: true,
    centerMode: true,
    centerPadding: "0px",
    variableWidth: false,
  };

  if (error) return <p>Error: {error}</p>;

  return (
    <div
      className="header-carousel position-relative"
      style={{
        width: "100%",
        maxWidth: "100vw",
        margin: "0 auto",
        overflow: "hidden",
        padding: "0",
      }}
    >
      <Slider {...settings}>
        {sliders.map((item, i) => (
          <div key={i}>
            {item.description ? (
              <a
                href={item.description}
                target="_blank"
                rel="noopener noreferrer"
              >
                <img
                  src={`http://127.0.0.1:8000${item.image}`}
                  alt={item.title || `Slide ${i + 1}`}
                  className="img-fluid w-100"
                  style={{
                    objectFit: "fill",
                    height: "400px",
                    cursor: "pointer",
                  }}
                />
              </a>
            ) : (
              <img
                src={`http://127.0.0.1:8000${item.image}`}
                alt={item.title || `Slide ${i + 1}`}
                className="img-fluid w-100"
                style={{ objectFit: "fill", height: "400px" }}
              />
            )}
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default HeroSlider;
