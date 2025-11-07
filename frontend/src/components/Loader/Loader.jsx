import React from "react";
import "./Loader.css"; // Import normal CSS

const Loader = () => {
  return (
    <div className="dot-spinner">
      <div className="dot-spinner__dot" />
      <div className="dot-spinner__dot" />
      <div className="dot-spinner__dot" />
      <div className="dot-spinner__dot" />
      <div className="dot-spinner__dot" />
      <div className="dot-spinner__dot" />
      <div className="dot-spinner__dot" />
      <div className="dot-spinner__dot" />
    </div>
  );
};

export default Loader;
