import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./AuthForm.css";

const Login = () => {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login Data:", form);
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2 className="auth-heading">Login</h2>
        <p className="auth-subtext">
          Welcome back! Sign in to continue your PTE preparation journey.
        </p>

        <div className="input-field">
          <input
            type="text"
            name="username"
            placeholder="Email or Mobile"
            value={form.username}
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

        <div className="btn-group">
          <button type="submit" className="auth-btn">Login</button>
        </div>

        <div className="auth-extra">
          <a href="#">Forgot Password?</a>
        </div>

        {/* 👇 Add tagline for navigation */}
        <p className="auth-toggle">
          Don’t have an account?{" "}
          <Link to="/signup">
            <span>Sign Up</span>
          </Link>
        </p>
      </form>
    </div>
  );
};

export default Login;
