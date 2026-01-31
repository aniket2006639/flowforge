import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PrdEditor from '../components/PrdEditor';
import TaskPreviewPanel from '../components/TaskPreviewPanel';
import KanbanBoard from '../components/KanbanBoard';
import StatusBanner from '../components/StatusBanner';
import DotGrid from '../components/DotGrid';
import { preview, pushSelected, fetchBoard } from '../api/pipelineApi';
import './Workspace.css';

function Workspace() {
  const navigate = useNavigate();
  const [prdText, setPrdText] = useState('');
  const [previewEpics, setPreviewEpics] = useState([]);
  const [selectedStories, setSelectedStories] = useState([]);
  const [board, setBoard] = useState(null);
  const [boardLoading, setBoardLoading] = useState(false);
  const [status, setStatus] = useState('idle');
  const [errorMessage, setErrorMessage] = useState(null);
  const [project, setProject] = useState('');
  const [issueKeys, setIssueKeys] = useState(null);
  const [createdCount, setCreatedCount] = useState(0);

  useEffect(() => {
    const storedProject = localStorage.getItem('project');
    if (storedProject) {
      setProject(storedProject);
      loadBoard(storedProject);
    }
  }, []);

  const loadBoard = async (projectKey) => {
    if (!projectKey) return;
    try {
      setBoardLoading(true);
      const boardData = await fetchBoard(projectKey);
      setBoard(boardData);
    } catch (error) {
      console.error('Failed to load board:', error);
    } finally {
      setBoardLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!project) {
      setStatus('error');
      setErrorMessage('Please set a project first');
      return;
    }

    setStatus('generating');
    setErrorMessage(null);
    setIssueKeys(null);
    setCreatedCount(0);

    try {
      const result = await preview(project, prdText);
      setPreviewEpics(result.epics || []);
      
      const allStoryIds = [];
      (result.epics || []).forEach((epic, epicIndex) => {
        (epic.stories || []).forEach((_, storyIndex) => {
          allStoryIds.push(`${epicIndex}-${storyIndex}`);
        });
      });
      setSelectedStories(allStoryIds);
      
      setStatus('idle');
    } catch (error) {
      setStatus('error');
      setErrorMessage(error.message || 'Failed to generate tasks');
    }
  };

  const handleSelectionChange = (newSelection) => {
    setSelectedStories(newSelection);
  };

  const handleStoryUpdate = (epicIndex, storyIndex, updatedStory) => {
    const newEpics = [...previewEpics];
    if (newEpics[epicIndex] && newEpics[epicIndex].stories) {
      newEpics[epicIndex].stories[storyIndex] = updatedStory;
      setPreviewEpics(newEpics);
    }
  };

  const handlePushSelected = async () => {
    if (!project) {
      setStatus('error');
      setErrorMessage('Please set a project first');
      return;
    }

    if (selectedStories.length === 0) {
      setStatus('error');
      setErrorMessage('Please select at least one story');
      return;
    }

    const tasksToPush = [];
    selectedStories.forEach((storyId) => {
      const [epicIndex, storyIndex] = storyId.split('-').map(Number);
      if (previewEpics[epicIndex] && previewEpics[epicIndex].stories[storyIndex]) {
        const story = previewEpics[epicIndex].stories[storyIndex];
        const task = {
          title: story.title || '',
          description: story.description || '',
          type: 'Task',
          subtasks: (story.subtasks || []).map(subtask => ({
            title: subtask.title || '',
            description: subtask.description || ''
          }))
        };

        if (story.acceptanceCriteria && story.acceptanceCriteria.length > 0) {
          task.acceptanceCriteria = story.acceptanceCriteria;
        } else if (story.acceptance_criteria && story.acceptance_criteria.length > 0) {
          task.acceptanceCriteria = story.acceptance_criteria;
        }

        if (story.priority) {
          task.priority = story.priority;
        }

        if (story.storyPoints) {
          task.storyPoints = story.storyPoints;
        } else if (story.story_points) {
          task.storyPoints = story.story_points;
        }

        tasksToPush.push(task);
      }
    });

    setStatus('pushing');
    setErrorMessage(null);

    try {
      const result = await pushSelected(project, tasksToPush);
      const count = result.created?.length || 0;
      setCreatedCount(count);
      
      if (count === 0) {
        setStatus('error');
        setErrorMessage('No issues were created. Please check your tasks and try again.');
        setIssueKeys(null);
      } else {
        const createdKeys = result.created?.map(item => item.key).filter(Boolean) || [];
        setIssueKeys(createdKeys);
        setStatus('success');
        setTimeout(() => loadBoard(project), 500);
      }
    } catch (error) {
      console.error('Push failed:', error);
      setStatus('error');
      setErrorMessage(error.message || 'Failed to push tasks');
      setIssueKeys(null);
      setCreatedCount(0);
    }
  };

  return (
    <div className="workspace">
      <div className="workspace-background">
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
      
      <div className="workspace-content">
        <header className="workspace-header">
          <div className="workspace-logo" onClick={() => navigate('/')}>
            FlowForge
          </div>
          <div className="workspace-header-controls">
            <input
              type="text"
              value={project}
              onChange={(e) => {
                const newProject = e.target.value;
                setProject(newProject);
                localStorage.setItem('project', newProject);
                if (newProject) {
                  loadBoard(newProject);
                }
              }}
              placeholder="Project Key"
              className="project-input"
            />
            {selectedStories.length > 0 && (
              <button
                className="push-selected-btn"
                onClick={handlePushSelected}
                disabled={status === 'pushing' || status === 'generating'}
              >
                {status === 'pushing' ? 'Pushing...' : `Push Selected (${selectedStories.length})`}
              </button>
            )}
          </div>
        </header>

        <StatusBanner
          status={status}
          issueKeys={issueKeys}
          errorMessage={errorMessage}
          createdCount={createdCount}
        />

        <main className="workspace-main">
          <div className="workspace-top-section">
            <div className="workspace-panel workspace-panel-left">
              <PrdEditor
                prdText={prdText}
                onPrdChange={setPrdText}
                onGenerate={handleGenerate}
                isLoading={status === 'generating'}
              />
            </div>

            <div className="workspace-panel workspace-panel-middle">
              <TaskPreviewPanel
                previewEpics={previewEpics}
                selectedStories={selectedStories}
                onSelectionChange={handleSelectionChange}
                onStoryUpdate={handleStoryUpdate}
              />
            </div>
          </div>

          <div className="workspace-bottom-section">
            <div className="workspace-panel workspace-panel-full">
              <KanbanBoard 
                board={board} 
                isLoading={boardLoading} 
                onRefresh={() => loadBoard(project)}
              />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Workspace;
