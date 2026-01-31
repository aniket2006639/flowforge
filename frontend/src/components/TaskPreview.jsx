import './TaskPreview.css';

function TaskPreview({ tasks }) {
  if (!tasks || !tasks.epics || tasks.epics.length === 0) {
    return null;
  }

  return (
    <div className="task-preview">
      <h2>Generated Tasks</h2>
      <div className="epics-container">
        {tasks.epics.map((epic, epicIndex) => (
          <div key={epicIndex} className="epic">
            <h3 className="epic-title">{epic.title || `Epic ${epicIndex + 1}`}</h3>
            {epic.description && (
              <p className="epic-description">{epic.description}</p>
            )}
            {epic.stories && epic.stories.length > 0 && (
              <ul className="stories-list">
                {epic.stories.map((story, storyIndex) => (
                  <li key={storyIndex} className="story">
                    <span className="story-title">{story.title || `Story ${storyIndex + 1}`}</span>
                    {story.description && (
                      <span className="story-description"> - {story.description}</span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default TaskPreview;
