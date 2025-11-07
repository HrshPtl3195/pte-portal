import React from "react";
import "./CustomButton.css";

const CustomButton = ({ label = "Click me!", onClick }) => {
  return (
    <button className="custom-btn" onClick={onClick}>
      {label}
    </button>
  );
};

export default CustomButton;
