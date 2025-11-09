import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";
import logo from "../../assets/pte-logo-new.jpg";
import profile from "../../assets/profile-pic.jpg";

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  const dropdownRef = useRef(null);
  const hoverTimeout = useRef(null);

  // ✅ Detect touch devices (phones, tablets)
  useEffect(() => {
    const checkTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    setIsTouchDevice(checkTouch);
  }, []);

  // ✅ Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // ✅ Hover handlers (for desktops/laptops)
  const handleMouseEnter = () => {
    if (!isTouchDevice) {
      clearTimeout(hoverTimeout.current);
      setDropdownOpen(true);
    }
  };

  const handleMouseLeave = () => {
    if (!isTouchDevice) {
      hoverTimeout.current = setTimeout(() => {
        setDropdownOpen(false);
      }, 150);
    }
  };

  // ✅ Click handler (for touch devices)
  const handleDropdownClick = (e) => {
    e.preventDefault();
    if (isTouchDevice) {
      setDropdownOpen((prev) => !prev);
    }
  };

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
          <Link to="/dashboard" onMouseEnter={() => setDropdownOpen(false)}>
            Dashboard
          </Link>

          {/* ---- PTE Practice Dropdown ---- */}
          <div
            className="dropdown"
            ref={dropdownRef}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            <div
              className="dropdown-link"
              onClick={handleDropdownClick}
            >
              PTE Practice ▾
            </div>

            <div
              className={`mega-dropdown ${dropdownOpen ? "show" : ""}`}
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              <h3 className="dropdown-title">
                Instant AI-Evaluated Predictive Questions
              </h3>

              <div className="dropdown-grid">
                {/* SPEAKING */}
                <div className="dropdown-column">
                  <h4 className="section-title">Speaking</h4>
                  <ul>
                    <li>Read Aloud</li>
                    <li>Repeat Sentence</li>
                    <li>Describe Image</li>
                    <li>Retell Lecture</li>
                    <li>Answer Short Question</li>
                    <li>
                      Summarize Group Discussion <span className="new">New</span>
                    </li>
                    <li>
                      Respond to a Situation <span className="new">New</span>
                    </li>
                  </ul>
                </div>

                {/* WRITING */}
                <div className="dropdown-column">
                  <h4 className="section-title">Writing</h4>
                  <ul>
                    <li>Summarize Written Text</li>
                    <li>Write Essay</li>
                  </ul>
                </div>

                {/* READING */}
                <div className="dropdown-column">
                  <h4 className="section-title">Reading</h4>
                  <ul>
                    <li>Multiple Choice, Single Answer</li>
                    <li>Multiple Choice, Multiple Answers</li>
                    <li>Reorder Paragraph</li>
                    <li>Fill in the Blanks (Drag & Drop)</li>
                    <li>Fill in the Blanks (Dropdown)</li>
                  </ul>
                </div>

                {/* LISTENING */}
                <div className="dropdown-column">
                  <h4 className="section-title">Listening</h4>
                  <ul>
                    <li>Summarize Spoken Text</li>
                    <li>Multiple Choice, Multiple Answers</li>
                    <li>Fill in the Blanks (Type In)</li>
                    <li>Highlight Correct Summary</li>
                    <li>Multiple Choice, Single Answer</li>
                    <li>Select Missing Word</li>
                    <li>Highlight Incorrect Words</li>
                    <li>Write from Dictation</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* ---- Other Links ---- */}
          <Link to="/online-tests" onMouseEnter={() => setDropdownOpen(false)}>
            Online Tests
          </Link>
          <Link to="/assigned-tests" onMouseEnter={() => setDropdownOpen(false)}>
            Assigned Tests
          </Link>
          <Link to="/test-history" onMouseEnter={() => setDropdownOpen(false)}>
            Test History
          </Link>
          <Link
            to="/assigned-courses"
            onMouseEnter={() => setDropdownOpen(false)}
          >
            Assigned Courses
          </Link>
          <Link to="/sessions" onMouseEnter={() => setDropdownOpen(false)}>
            Online Sessions
          </Link>
        </div>

        {/* ---- Right: Profile ---- */}
        <div className="nav-right">
          <Link to="/profile" className="profile-link">
            <img src={profile} alt="Profile" className="profile-icon" />
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
