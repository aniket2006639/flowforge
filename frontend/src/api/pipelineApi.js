import apiRequest from './apiClient';

export async function preview(project, prd) {
  return apiRequest('/pipeline/preview', {
    method: 'POST',
    body: JSON.stringify({ project, prd }),
  });
}

export async function pushSelected(project, tasks) {
  return apiRequest('/pipeline/push-selected', {
    method: 'POST',
    body: JSON.stringify({ project, tasks }),
  });
}

export async function fetchBoard(project) {
  return apiRequest(`/jira/issues?project=${encodeURIComponent(project)}`, {
    method: 'GET',
  });
}

export async function getTransitions(issueKey) {
  return apiRequest(`/jira/issue/${issueKey}/transitions`, {
    method: 'GET',
  });
}

export async function transitionIssue(issueKey, transitionId) {
  return apiRequest(`/jira/issue/${issueKey}/transition/${transitionId}`, {
    method: 'POST',
  });
}
