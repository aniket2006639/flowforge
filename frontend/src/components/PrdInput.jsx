import { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import './PrdInput.css';

function PrdInput({ onGenerate, isLoading }) {
  const [prd, setPrd] = useState('');
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      gsap.fromTo(
        containerRef.current,
        {
          opacity: 0,
          y: 30,
          scale: 0.95,
        },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.6,
          ease: 'power3.out',
          delay: 0.1,
        }
      );
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prd.trim() && !isLoading) {
      onGenerate(prd.trim());
    }
  };

  return (
    <div ref={containerRef} className="prd-input-wrapper">
      <div className="prd-input">
        <h2>Product Idea / PRD</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            value={prd}
            onChange={(e) => setPrd(e.target.value)}
            placeholder="Paste your product idea or PRD here..."
            rows={12}
            disabled={isLoading}
            className="prd-textarea"
          />
          <button type="submit" disabled={!prd.trim() || isLoading}>
            {isLoading ? 'Generating Tasks...' : 'Generate Tasks'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default PrdInput;
