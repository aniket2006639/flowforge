import './PrdEditor.css';

function PrdEditor({ onGenerate, isLoading, prdText, onPrdChange }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (prdText.trim() && !isLoading) {
      onGenerate(prdText.trim());
    }
  };

  return (
    <div className="prd-editor-panel">
      <h2 className="panel-title">PRD Input</h2>
      <form onSubmit={handleSubmit} className="prd-editor-form">
        <textarea
          value={prdText}
          onChange={(e) => onPrdChange(e.target.value)}
          placeholder="Paste your product requirement document here..."
          rows={20}
          disabled={isLoading}
          className="prd-editor-textarea"
        />
        <button 
          type="submit" 
          disabled={!prdText.trim() || isLoading}
          className="generate-tasks-btn"
        >
          {isLoading ? 'Generating...' : 'Generate Tasks'}
        </button>
      </form>
    </div>
  );
}

export default PrdEditor;
