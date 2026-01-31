import './StatusBanner.css';

const STATUS_MESSAGES = {
  idle: null,
  generating: 'Generating tasks from your PRD...',
  pushing: 'Pushing tasks to Jira...',
  success: (count) => `Created ${count} issue${count !== 1 ? 's' : ''} successfully`,
  error: (message) => message || 'An error occurred. Please try again.',
};

function StatusBanner({ status, issueKeys, errorMessage, createdCount }) {
  if (status === 'idle') {
    return null;
  }

  const getMessage = () => {
    if (status === 'success') {
      const count = createdCount !== undefined ? createdCount : (issueKeys?.length || 0);
      return STATUS_MESSAGES.success(count);
    }
    if (status === 'error') {
      return STATUS_MESSAGES.error(errorMessage);
    }
    return STATUS_MESSAGES[status];
  };

  const getStatusClass = () => {
    if (status === 'error') return 'error';
    if (status === 'success') return 'success';
    return 'info';
  };

  return (
    <div className={`status-banner ${getStatusClass()}`}>
      <div className="status-content">
        {status === 'generating' || status === 'pushing' ? (
          <span className="status-spinner">⏳</span>
        ) : status === 'success' ? (
          <span className="status-icon">✓</span>
        ) : status === 'error' ? (
          <span className="status-icon">✗</span>
        ) : null}
        <span className="status-message">{getMessage()}</span>
      </div>
      {status === 'success' && issueKeys && issueKeys.length > 0 && (
        <div className="issue-keys">
          <strong>Created Issues:</strong> {issueKeys.join(', ')}
        </div>
      )}
    </div>
  );
}

export default StatusBanner;
