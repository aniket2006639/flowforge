const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

/**
 * Generate tasks from a PRD (proxy to pipeline preview)
 * @param {string} project - The project key to preview generation for
 * @param {string} prd - The product requirement document text
 * @returns {Promise<{epics: Array}>} Structured tasks with epics and stories
 */
export async function generateTasks(project, prd) {
  const response = await fetch(`${API_BASE_URL}/pipeline/preview`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ project, prd }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Failed to generate tasks' }));
    throw new Error(error.message || 'Failed to generate tasks');
  }

  return response.json();
}

/**
 * Push tasks to Jira
 * @param {Object} params - Parameters object
 * @param {Array} params.tasks - The tasks to push (epics and stories)
 * @param {string} params.jiraBaseUrl - Jira instance base URL
 * @param {string} params.email - Jira user email
 * @param {string} params.apiToken - Jira API token
 * @returns {Promise<{issueKeys: Array<string>}>} Created Jira issue keys
 */
export async function pushToJira({ tasks, jiraBaseUrl, email, apiToken }) {
  const response = await fetch(`${API_BASE_URL}/push-to-jira`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      tasks,
      jiraBaseUrl,
      email,
      apiToken,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Failed to push to Jira' }));
    throw new Error(error.message || 'Failed to push to Jira');
  }

  return response.json();
}
