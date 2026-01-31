import { useState, useEffect } from 'react';
import './StoryCard.css';

function StoryCard({ story, isSelected, onToggleSelect, onUpdate }) {
  const [localStory, setLocalStory] = useState({
    title: story.title || '',
    description: story.description || '',
    acceptanceCriteria: story.acceptanceCriteria || story.acceptance_criteria || [],
    priority: story.priority || 'Medium',
    storyPoints: story.storyPoints || story.story_points || 3,
    subtasks: story.subtasks || [],
    ...story
  });

  useEffect(() => {
    setLocalStory({
      title: story.title || '',
      description: story.description || '',
      acceptanceCriteria: story.acceptanceCriteria || story.acceptance_criteria || [],
      priority: story.priority || 'Medium',
      storyPoints: story.storyPoints || story.story_points || 3,
      subtasks: story.subtasks || [],
      ...story
    });
  }, [story]);

  const updateStory = (updates) => {
    const updated = { ...localStory, ...updates };
    setLocalStory(updated);
    onUpdate(updated);
  };

  const handleTitleChange = (e) => {
    updateStory({ title: e.target.value });
  };

  const handleDescriptionChange = (e) => {
    updateStory({ description: e.target.value });
  };

  const handleAcceptanceCriteriaChange = (index, value) => {
    const newCriteria = [...localStory.acceptanceCriteria];
    newCriteria[index] = value;
    updateStory({ acceptanceCriteria: newCriteria });
  };

  const addAcceptanceCriteria = () => {
    updateStory({ acceptanceCriteria: [...localStory.acceptanceCriteria, ''] });
  };

  const removeAcceptanceCriteria = (index) => {
    const newCriteria = localStory.acceptanceCriteria.filter((_, i) => i !== index);
    updateStory({ acceptanceCriteria: newCriteria });
  };

  const handlePriorityChange = (e) => {
    updateStory({ priority: e.target.value });
  };

  const handleStoryPointsChange = (e) => {
    updateStory({ storyPoints: parseInt(e.target.value) || 3 });
  };

  const handleSubtaskTitleChange = (index, value) => {
    const newSubtasks = [...localStory.subtasks];
    newSubtasks[index] = { ...newSubtasks[index], title: value };
    updateStory({ subtasks: newSubtasks });
  };

  const handleSubtaskDescriptionChange = (index, value) => {
    const newSubtasks = [...localStory.subtasks];
    newSubtasks[index] = { ...newSubtasks[index], description: value };
    updateStory({ subtasks: newSubtasks });
  };

  const addSubtask = () => {
    updateStory({ subtasks: [...localStory.subtasks, { title: '', description: '' }] });
  };

  const removeSubtask = (index) => {
    const newSubtasks = localStory.subtasks.filter((_, i) => i !== index);
    updateStory({ subtasks: newSubtasks });
  };

  return (
    <div className="story-card">
      <div className="story-card-header">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={onToggleSelect}
          className="story-checkbox"
        />
        <input
          type="text"
          value={localStory.title}
          onChange={handleTitleChange}
          className="story-title-input"
          placeholder="Story title"
        />
      </div>

      <textarea
        value={localStory.description}
        onChange={handleDescriptionChange}
        className="story-description-input"
        placeholder="Story description"
        rows={3}
      />

      <div className="story-meta-fields">
        <div className="story-field-group">
          <label className="story-field-label">Priority</label>
          <select
            value={localStory.priority}
            onChange={handlePriorityChange}
            className="story-select-input"
          >
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>

        <div className="story-field-group">
          <label className="story-field-label">Story Points</label>
          <select
            value={localStory.storyPoints}
            onChange={handleStoryPointsChange}
            className="story-select-input"
          >
            <option value={1}>1</option>
            <option value={2}>2</option>
            <option value={3}>3</option>
            <option value={5}>5</option>
            <option value={8}>8</option>
          </select>
        </div>
      </div>

      <div className="story-acceptance-criteria">
        <div className="story-section-header">
          <strong>Acceptance Criteria</strong>
          <button
            type="button"
            onClick={addAcceptanceCriteria}
            className="story-add-btn"
            title="Add acceptance criteria"
          >
            +
          </button>
        </div>
        {localStory.acceptanceCriteria.length === 0 ? (
          <p className="story-empty-hint">No acceptance criteria. Click + to add.</p>
        ) : (
          <ul className="story-criteria-list">
            {localStory.acceptanceCriteria.map((criteria, idx) => (
              <li key={idx} className="story-criteria-item">
                <input
                  type="text"
                  value={criteria}
                  onChange={(e) => handleAcceptanceCriteriaChange(idx, e.target.value)}
                  className="story-criteria-input"
                  placeholder="Enter acceptance criteria"
                />
                <button
                  type="button"
                  onClick={() => removeAcceptanceCriteria(idx)}
                  className="story-remove-btn"
                  title="Remove"
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="story-subtasks">
        <div className="story-section-header">
          <strong>Subtasks</strong>
          <button
            type="button"
            onClick={addSubtask}
            className="story-add-btn"
            title="Add subtask"
          >
            + Add Subtask
          </button>
        </div>
        {localStory.subtasks.length === 0 ? (
          <p className="story-empty-hint">No subtasks. Click + Add Subtask to create.</p>
        ) : (
          <div className="story-subtasks-list">
            {localStory.subtasks.map((subtask, idx) => (
              <div key={idx} className="story-subtask-item">
                <input
                  type="text"
                  value={subtask.title || ''}
                  onChange={(e) => handleSubtaskTitleChange(idx, e.target.value)}
                  className="story-subtask-title-input"
                  placeholder="Subtask title"
                />
                <textarea
                  value={subtask.description || ''}
                  onChange={(e) => handleSubtaskDescriptionChange(idx, e.target.value)}
                  className="story-subtask-description-input"
                  placeholder="Subtask description"
                  rows={2}
                />
                <button
                  type="button"
                  onClick={() => removeSubtask(idx)}
                  className="story-remove-btn"
                  title="Remove subtask"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default StoryCard;
