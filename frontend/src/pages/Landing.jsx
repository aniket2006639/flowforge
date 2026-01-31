import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import JiraLoginModal from '../components/JiraLoginModal';
import DotGrid from '../components/DotGrid';
import { login, signup, connectJira } from '../api/apiClient';
import './Landing.css';

function Landing() {
  const navigate = useNavigate();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showEmail, setShowEmail] = useState(false);

  const handleGetStarted = () => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/workspace');
    } else {
      setShowLoginModal(true);
    }
  };

  const handleLoginWithJira = () => {
    setShowLoginModal(true);
  };

  const handleLogin = async (credentials) => {
    setIsLoading(true);
    try {
      try {
        await login(credentials);
      } catch {
        await signup(credentials);
      }
      await connectJira(credentials);
      setShowLoginModal(false);
      navigate('/workspace');
    } catch (error) {
      alert(error.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="landing">
      <div className="background-layer">
        <DotGrid
          dotSize={3}
          gap={40}
          baseColor="#ffffff"
          activeColor="#0065ff"
          proximity={90}
          shockRadius={0}
          shockStrength={0}
          resistance={1200}
          returnDuration={2.5}
        />
      </div>
      <div className="foreground-content">
        {/* HEADER */}
        <div className="landing-header">
        <div className="landing-logo">
          <div className="logo-title">FlowForge</div>
          <div className="logo-subtitle">Powered by YuktiX</div>
        </div>

        <button className="login-jira-btn" onClick={handleLoginWithJira}>
          Login with Jira
        </button>
      </div>

      {/* CONTENT */}
      <div className="landing-content">
        <h1 className="landing-tagline">
          Write the idea. We build the backlog.
        </h1>

        <div className="landing-flow">
          <span>Write</span>
          <span className="arrow">→</span>
          <span>Generate</span>
          <span className="arrow">→</span>
          <span>Push to Jira</span>
        </div>
      </div>

      {/* ACTION */}
      <div className="landing-action">
        <button className="get-started-btn" onClick={handleGetStarted}>
          Get Started
        </button>
      </div>

      {/* FOOTER */}
      <footer className="landing-footer">
        <span>© {new Date().getFullYear()} YuktiX. All rights reserved.</span>

        <button
          className="contact-btn"
          onClick={() => setShowEmail(!showEmail)}
        >
          Contact Us
        </button>

        {showEmail && (
          <span className="contact-email">info@yuktix.net</span>
        )}
      </footer>

        <JiraLoginModal
          isOpen={showLoginModal}
          onClose={() => setShowLoginModal(false)}
          onLogin={handleLogin}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}

export default Landing;
