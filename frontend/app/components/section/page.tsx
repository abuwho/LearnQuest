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
      {section.title}
      {isExpanded && (
        <ul className="lesson-list">
          {section.lessons.map((lesson) => (
            <li key={lesson.id} className="lesson-item">
               {/*TODO:  fix routing here */}
              <Link href={`/lessons/${lesson.id}`}>
                <span>{lesson.title}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Section;