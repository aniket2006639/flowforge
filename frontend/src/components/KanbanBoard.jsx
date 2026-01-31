import { useState } from 'react';
import IssueCard from './IssueCard';
import { getTransitions, transitionIssue } from '../api/pipelineApi';
import './KanbanBoard.css';

function KanbanBoard({ board, isLoading, onRefresh }) {
  const [transitioningIssues, setTransitioningIssues] = useState(new Set());
  const [transitionError, setTransitionError] = useState(null);

  const handleTransition = async (issueKey, targetStatus) => {
    setTransitioningIssues(prev => new Set(prev).add(issueKey));
    setTransitionError(null);

    try {
      const transitionsResponse = await getTransitions(issueKey);
      const transitions = transitionsResponse.transitions || [];
      
      const statusMap = {
        'Backlog': ['backlog', 'to do', 'todo'],
        'Selected for Development': ['selected for development', 'in progress', 'in development', 'development'],
        'Done': ['done', 'completed', 'complete', 'closed']
      };

      const targetKeywords = statusMap[targetStatus] || [targetStatus.toLowerCase()];
      
      const matchingTransition = transitions.find(t => {
        const transitionName = t.name.toLowerCase();
        return targetKeywords.some(keyword => transitionName.includes(keyword));
      });

      if (!matchingTransition) {
        throw new Error(`Transition to "${targetStatus}" not available for this issue`);
      }

      await transitionIssue(issueKey, matchingTransition.id);
      
      if (onRefresh) {
        setTimeout(() => onRefresh(), 300);
      }
    } catch (error) {
      console.error('Transition failed:', error);
      setTransitionError(error.message || 'Failed to transition issue');
      setTimeout(() => setTransitionError(null), 5000);
    } finally {
      setTransitioningIssues(prev => {
        const next = new Set(prev);
        next.delete(issueKey);
        return next;
      });
    }
  };

  if (isLoading) {
    return (
      <div className="kanban-board-panel">
        <h2 className="panel-title">Kanban Board</h2>
        <div className="board-loading">
          <p>Loading board...</p>
        </div>
      </div>
    );
  }

  if (!board) {
    return (
      <div className="kanban-board-panel">
        <h2 className="panel-title">Kanban Board</h2>
        <div className="empty-board">
          <p>No board data available</p>
        </div>
      </div>
    );
  }

  const columns = board.columns || [];
  const columnMap = {
    'Backlog': 'Backlog',
    'Selected for Development': 'Selected for Development',
    'Done': 'Done',
  };

  const getColumnIssues = (columnName) => {
    if (!columns || columns.length === 0) {
      if (board.issues && Array.isArray(board.issues)) {
        return board.issues.filter(issue => {
          const status = issue.status || issue.fields?.status?.name || '';
          return status.toLowerCase().includes(columnName.toLowerCase());
        });
      }
      return [];
    }
    const column = columns.find(col => 
      col.name === columnName || 
      col.name?.toLowerCase() === columnName.toLowerCase()
    );
    return column?.issues || [];
  };

  return (
    <div className="kanban-board-panel">
      <div className="kanban-board-header">
        <h2 className="panel-title">Kanban Board</h2>
        {transitionError && (
          <div className="transition-error-banner">
            {transitionError}
          </div>
        )}
      </div>
      <div className="kanban-board">
        {Object.values(columnMap).map((columnName) => {
          const issues = getColumnIssues(columnName);
          return (
            <div key={columnName} className="kanban-column">
              <div className="column-header">
                <h3 className="column-title">{columnName}</h3>
                <span className="column-count">{issues.length}</span>
              </div>
              <div className="column-issues">
                {issues.length === 0 ? (
                  <div className="empty-column">No issues</div>
                ) : (
                  issues.map((issue, idx) => {
                    const issueKey = issue.key || issue.id || `ISSUE-${idx}`;
                    const isTransitioning = transitioningIssues.has(issueKey);
                    return (
                      <IssueCard
                        key={issueKey || idx}
                        issue={issue}
                        onTransition={handleTransition}
                        isTransitioning={isTransitioning}
                      />
                    );
                  })
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default KanbanBoard;
