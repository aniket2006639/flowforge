const API_BASE_URL = 'http://127.0.0.1:8000';

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = token;
  }

  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      localStorage.removeItem('token');
      throw new Error('Unauthorized. Please login again.');
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ 
        detail: response.statusText || 'Request failed' 
      }));
      throw new Error(error.detail || error.message || 'Request failed');
    }

    return response.json();
  } catch (error) {
    console.error('API request failed:', error);
    
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error(`Cannot connect to backend at ${API_BASE_URL}. Please ensure the backend server is running.`);
    }
    
    if (error.message) {
      throw error;
    }
    
    throw new Error('Network error. Please check your connection and ensure the backend is running.');
  }
}

export async function signup(credentials) {
  const response = await apiRequest('/auth/signup', {
    method: 'POST',
    body: JSON.stringify({
      email: credentials.email,
      password: credentials.apiToken,
    }),
  });
  
  if (response.access_token) {
    localStorage.setItem('token', `Bearer ${response.access_token}`);
  }
  
  return response;
}

export async function login(credentials) {
  const response = await apiRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      email: credentials.email,
      password: credentials.apiToken,
    }),
  });
  
  if (response.access_token) {
    localStorage.setItem('token', `Bearer ${response.access_token}`);
  }
  
  return response;
}

export async function connectJira(jiraCredentials) {
  return apiRequest('/jira/connect', {
    method: 'POST',
    body: JSON.stringify({
      site_url: jiraCredentials.jiraBaseUrl,
      email: jiraCredentials.email,
      api_token: jiraCredentials.apiToken,
    }),
  });
}

export default apiRequest;
