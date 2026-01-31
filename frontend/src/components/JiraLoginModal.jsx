import { useState } from 'react';
import './JiraLoginModal.css';

function JiraLoginModal({ isOpen, onClose, onLogin, isLoading }) {
  const [jiraBaseUrl, setJiraBaseUrl] = useState('');
  const [email, setEmail] = useState('');
  const [apiToken, setApiToken] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (jiraBaseUrl.trim() && email.trim() && apiToken.trim() && !isLoading) {
      onLogin({
        jiraBaseUrl: jiraBaseUrl.trim(),
        email: email.trim(),
        apiToken: apiToken.trim(),
      });
    }
  };

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="jira-modal-backdrop" onClick={handleBackdropClick}>
      <div className="jira-modal">
        <div className="jira-modal-header">
          <h2>Login with Jira</h2>
          <button className="jira-modal-close" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit} className="jira-modal-form">
          <div className="form-group">
            <label htmlFor="jiraBaseUrl">Jira Base URL</label>
            <input
              id="jiraBaseUrl"
              type="url"
              value={jiraBaseUrl}
              onChange={(e) => setJiraBaseUrl(e.target.value)}
              placeholder="https://yourcompany.atlassian.net"
              disabled={isLoading}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Jira Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your.email@example.com"
              disabled={isLoading}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="apiToken">Jira API Token</label>
            <input
              id="apiToken"
              type="password"
              value={apiToken}
              onChange={(e) => setApiToken(e.target.value)}
              placeholder="Enter your Jira API token"
              disabled={isLoading}
              required
            />
          </div>
          <div className="jira-modal-actions">
            <button type="button" onClick={onClose} className="jira-modal-cancel">
              Cancel
            </button>
            <button
              type="submit"
              disabled={!jiraBaseUrl.trim() || !email.trim() || !apiToken.trim() || isLoading}
              className="jira-modal-submit"
            >
              {isLoading ? 'Connecting...' : 'Connect'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default JiraLoginModal;
