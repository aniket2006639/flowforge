# PRD to Jira - Frontend Demo

A polished MVP frontend demo that converts product ideas (PRDs) into structured Jira tasks.

## Features

- **PRD Input**: Paste your product idea or PRD
- **Task Generation**: Automatically generate structured tasks grouped as Epics and Stories
- **Jira Integration**: Push generated tasks directly to Jira
- **Status Tracking**: Clear visual feedback throughout the process

## Tech Stack

- React (JavaScript)
- Vite
- Functional components with hooks
- Fetch API for backend communication

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

## Backend Integration

The app expects a backend API with the following endpoints:

- `POST /api/pipeline/preview` - Generates preview of tasks from a PRD (server-side PRD→Jira service)
  - Input: `{ prd: string }`
  - Output: `{ epics: Array<{ title: string, description?: string, stories: Array<{ title: string, description?: string }> }> }`

- `POST /api/push-to-jira` - Pushes tasks to Jira
  - Input: `{ tasks: Object, jiraBaseUrl: string, email: string, apiToken: string }`
  - Output: `{ issueKeys: Array<string> }`

### Environment Variables

Create a `.env` file in the root directory:

```
VITE_API_BASE_URL=http://localhost:3000/api
```

If not set, it defaults to `http://localhost:3000/api`.

## Project Structure

```
src/
  ├── components/
  │   ├── PrdInput.jsx          # PRD input form
  │   ├── TaskPreview.jsx       # Task preview display
  │   ├── JiraForm.jsx          # Jira credentials form
  │   └── StatusBanner.jsx      # Status display
  ├── api/
  │   └── jiraApi.js           # API integration layer
  ├── App.jsx                   # Main container component
  ├── main.jsx                  # Entry point
  └── index.css                 # Global styles
```

## Usage Flow

1. Paste your product idea or PRD into the text area
2. Click "Generate Tasks" to create structured tasks
3. Review the generated Epics and Stories
4. Enter your Jira credentials (Base URL, Email, API Token)
5. Click "Push to Jira" to create issues
6. View the created Jira issue keys in the status banner

## Notes

- This is a demo MVP, not a production application
- Mock data can be used if the backend is unavailable
- The UI is designed to be clear and easy to understand
- Styling is minimal and can be enhanced later
