import { useState } from 'react';
import './IssueCard.css';

function IssueCard({ issue, onTransition, isTransitioning }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const issueKey = issue.key || issue.id || 'UNKNOWN';
  const issueTitle = issue.title || issue.summary || issue.fields?.summary || 'Untitled';
  const issueDescription = issue.description || issue.fields?.description || '';
  const issueStatus = issue.status || issue.fields?.status?.name || 'Unknown';
  const issueSubtasks = issue.subtasks || issue.fields?.subtasks || [];

  const availableTransitions = [
    { name: 'Backlog', value: 'Backlog' },
    { name: 'Selected for Development', value: 'Selected for Development' },
    { name: 'Done', value: 'Done' }
  ];

  const handleTransition = (e) => {
    e.stopPropagation();
    const newStatus = e.target.value;
    if (newStatus && newStatus !== issueStatus && onTransition) {
      onTransition(issueKey, newStatus);
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div 
      className={`issue-card ${isExpanded ? 'expanded' : ''}`}
      onClick={toggleExpand}
    >
      <div className="issue-card-header">
        <div className="issue-key">{issueKey}</div>
        {isExpanded && (
          <button
            className="issue-expand-toggle"
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded(false);
            }}
            title="Collapse"
          >
            −
          </button>
        )}
      </div>

      <div className="issue-title">{issueTitle}</div>

      {isExpanded && (
        <div className="issue-expanded-content">
          {issueDescription && (
            <div className="issue-description">
              <strong>Description:</strong>
              <div className="issue-description-text">
                {typeof issueDescription === 'string' 
                  ? issueDescription 
                  : JSON.stringify(issueDescription)}
              </div>
            </div>
          )}

          {issueSubtasks && issueSubtasks.length > 0 && (
            <div className="issue-subtasks">
              <strong>Subtasks:</strong>
              <ul className="issue-subtasks-list">
                {issueSubtasks.map((subtask, idx) => (
                  <li key={idx}>
                    {subtask.key || subtask.id || `Subtask ${idx + 1}`}: {subtask.summary || subtask.title || 'Untitled'}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="issue-metadata">
            <div className="issue-metadata-item">
              <strong>Status:</strong> {issueStatus}
            </div>
            <div className="issue-metadata-item">
              <strong>Key:</strong> {issueKey}
            </div>
          </div>
        </div>
      )}

      <div className="issue-actions" onClick={(e) => e.stopPropagation()}>
        <select
          value={issueStatus}
          onChange={handleTransition}
          disabled={isTransitioning}
          className="issue-transition-select"
        >
          {availableTransitions.map(transition => (
            <option key={transition.value} value={transition.value}>
              {transition.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default IssueCard;
