import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";
import logo from "../../assets/pte-logo-new.jpg";
import profile from "../../assets/profile-pic.jpg";

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="nav-container">
        {/* ---- Left: Logo ---- */}
        <div className="nav-left">
          <Link to="/" className="logo">
            <img src={logo} alt="PTE Portal Logo" className="pte-logo" />
          </Link>
        </div>

        {/* ---- Center: Navigation ---- */}
        <div className={`nav-center ${menuOpen ? "active" : ""}`}>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/practice">PTE Practice</Link>
          <Link to="/online-tests">Online Tests</Link>
          <Link to="/assigned-tests">Assigned Tests</Link>
          <Link to="/test-history">Test History</Link>
          <Link to="/assigned-courses">Assigned Courses</Link>
          <Link to="/sessions">Online Sessions</Link>
        </div>

        {/* ---- Right: Profile ---- */}
        <div className="nav-right">
          <Link to="/profile" className="profile-link">
            <img
              src={profile}
              alt="Profile"
              className="profile-icon"
            />
          </Link>

          {/* Hamburger Icon */}
          <div
            className={`menu-icon ${menuOpen ? "open" : ""}`}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <div className="bar"></div>
            <div className="bar"></div>
            <div className="bar"></div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
