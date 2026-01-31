import { useState, useEffect } from 'react';
import StoryCard from './StoryCard';
import './TaskPreviewPanel.css';

function TaskPreviewPanel({ previewEpics, selectedStories, onSelectionChange, onStoryUpdate }) {
  const [localSelected, setLocalSelected] = useState(new Set(selectedStories));

  useEffect(() => {
    setLocalSelected(new Set(selectedStories));
  }, [selectedStories]);

  const toggleStory = (epicIndex, storyIndex) => {
    const storyId = `${epicIndex}-${storyIndex}`;
    const newSelected = new Set(localSelected);
    if (newSelected.has(storyId)) {
      newSelected.delete(storyId);
    } else {
      newSelected.add(storyId);
    }
    setLocalSelected(newSelected);
    onSelectionChange(Array.from(newSelected));
  };

  const handleStoryUpdate = (epicIndex, storyIndex, updatedStory) => {
    onStoryUpdate(epicIndex, storyIndex, updatedStory);
  };

  if (!previewEpics || previewEpics.length === 0) {
    return (
      <div className="task-preview-panel">
        <h2 className="panel-title">AI Preview</h2>
        <div className="empty-preview">
          <p>Generate tasks to see preview</p>
        </div>
      </div>
    );
  }

  return (
    <div className="task-preview-panel">
      <h2 className="panel-title">AI Preview</h2>
      <div className="preview-content">
        {previewEpics.map((epic, epicIndex) => (
          <div key={epicIndex} className="preview-epic">
            <h3 className="epic-title">{epic.title || `Epic ${epicIndex + 1}`}</h3>
            {epic.description && (
              <p className="epic-description">{epic.description}</p>
            )}
            {epic.stories && epic.stories.length > 0 && (
              <div className="stories-container">
                {epic.stories.map((story, storyIndex) => {
                  const storyId = `${epicIndex}-${storyIndex}`;
                  return (
                    <StoryCard
                      key={storyIndex}
                      story={story}
                      isSelected={localSelected.has(storyId)}
                      onToggleSelect={() => toggleStory(epicIndex, storyIndex)}
                      onUpdate={(updatedStory) => handleStoryUpdate(epicIndex, storyIndex, updatedStory)}
                    />
                  );
                })}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default TaskPreviewPanel;
