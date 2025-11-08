import React, { useState } from "react";
import "./AuthForm.css";

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);

  const toggleForm = () => setIsLogin(!isLogin);

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2 className="auth-heading">{isLogin ? "Login" : "Sign Up"}</h2>
        <p className="auth-subtext">
          {isLogin
            ? "Welcome back! Please log in to continue."
            : "Create your account to get started."}
        </p>

        {/* --- LOGIN FORM --- */}
        {isLogin ? (
          <>
            <div className="input-field">
              <input type="text" placeholder="Email or Mobile" />
            </div>
            <div className="input-field">
              <input type="password" placeholder="Password" />
            </div>
            <div className="btn-group">
              <button className="auth-btn">Login</button>
            </div>
            <div className="auth-extra">
              <a href="#">Forgot Password?</a>
            </div>
          </>
        ) : (
          /* --- SIGNUP FORM --- */
          <>
            <div className="input-row">
              <div className="input-field">
                <input type="text" placeholder="First Name" />
              </div>
              <div className="input-field">
                <input type="text" placeholder="Last Name" />
              </div>
            </div>
            <div className="input-field">
              <input type="email" placeholder="Email ID" />
            </div>
            <div className="input-field">
              <input type="tel" placeholder="Phone Number" />
            </div>
            <div className="input-field">
              <input type="password" placeholder="Password" />
            </div>
            <div className="input-field">
              <input type="password" placeholder="Confirm Password" />
            </div>
            <div className="btn-group">
              <button className="auth-btn">Sign Up</button>
            </div>
          </>
        )}

        <p className="auth-toggle">
          {isLogin ? (
            <>
              Don’t have an account?{" "}
              <span onClick={toggleForm}>Sign Up</span>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <span onClick={toggleForm}>Login</span>
            </>
          )}
        </p>
      </div>
    </div>
  );
};

export default AuthPage;
