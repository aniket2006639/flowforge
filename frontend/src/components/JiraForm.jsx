import { useState } from 'react';
import './JiraForm.css';

function JiraForm({ onPush, hasTasks, isLoading }) {
  const [jiraBaseUrl, setJiraBaseUrl] = useState('');
  const [email, setEmail] = useState('');
  const [apiToken, setApiToken] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (jiraBaseUrl.trim() && email.trim() && apiToken.trim() && !isLoading) {
      onPush({
        jiraBaseUrl: jiraBaseUrl.trim(),
        email: email.trim(),
        apiToken: apiToken.trim(),
      });
    }
  };

  return (
    <div className="jira-form">
      <h2>Jira Credentials</h2>
      <form onSubmit={handleSubmit}>
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
          <label htmlFor="email">Email</label>
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
          <label htmlFor="apiToken">API Token</label>
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
        <button
          type="submit"
          disabled={!hasTasks || !jiraBaseUrl.trim() || !email.trim() || !apiToken.trim() || isLoading}
        >
          {isLoading ? 'Pushing to Jira...' : 'Push to Jira'}
        </button>
      </form>
    </div>
  );
}

export default JiraForm;
