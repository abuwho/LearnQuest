import React, { useState } from "react";
import Link from 'next/link';
import './section.css';

const Section = ({ section }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const handleExpandClick = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div onClick={handleExpandClick} className="section">
      <h3>{section.title}</h3>
      {isExpanded && (
        <ul className="lesson-list">
          {section.lessons.map((lesson) => (
            <li key={lesson.id} className="lesson-item">
              <Link href={`/lessons/${lesson.id}`}>
                <a>{lesson.title}</a>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Section;