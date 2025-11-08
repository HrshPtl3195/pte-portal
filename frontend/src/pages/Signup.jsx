import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./AuthForm.css";

const Signup = () => {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Signup Data:", form);
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2 className="auth-heading">Sign Up</h2>
        <p className="auth-subtext">
          Create your account to start your PTE preparation journey.
        </p>

        <div className="input-row">
          <div className="input-field">
            <input
              type="text"
              name="firstName"
              placeholder="First Name"
              value={form.firstName}
              onChange={handleChange}
            />
          </div>
          <div className="input-field">
            <input
              type="text"
              name="lastName"
              placeholder="Last Name"
              value={form.lastName}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="input-field">
          <input
            type="email"
            name="email"
            placeholder="Email ID"
            value={form.email}
            onChange={handleChange}
          />
        </div>

        <div className="input-field">
          <input
            type="tel"
            name="phone"
            placeholder="Phone Number"
            value={form.phone}
            onChange={handleChange}
          />
        </div>

        <div className="input-field">
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
          />
        </div>

        <div className="input-field">
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={form.confirmPassword}
            onChange={handleChange}
          />
        </div>

        <div className="btn-group">
          <button type="submit" className="auth-btn">Sign Up</button>
        </div>

        {/* 👇 Tagline for Login */}
        <p className="auth-toggle">
          Already have an account?{" "}
          <Link to="/login">
            <span>Login</span>
          </Link>
        </p>
      </form>
    </div>
  );
};

export default Signup;
