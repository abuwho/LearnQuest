import React, { useState } from "react";
import Link from "next/link";
import "./section.css";
import { useRouter } from "next/navigation";

interface Lesson {
  id: string;
  duration: string;
  title: string;
  type: string;
  pdf?: string;
  video_url?: string;
  summary: string;
  created_at: string;
  updated_at: string;
  section: string;
}

interface IResponseGetLessons {
  id: string;
  duration: string;
  lessons: Lesson[];
  course: string;
  title: string;
  created_at: string;
  updated_at: string;
}

const Section = ({
  section,
  isAuthorized,
  isCreator,
}: {
  section: IResponseGetLessons;
  isAuthorized: boolean;
  isCreator: boolean;
}) => {
  const router = useRouter();
  const [isExpanded, setIsExpanded] = useState(false);

  const handleExpandClick = () => {
    if (!isAuthorized) return;
    setIsExpanded(!isExpanded);
  };

  const onUpdate = () => {
    router.push(`/course/${section.course}/section/${section.id}/update`);
  };

  const handleCreateLesson = () => {
    router.push(`/course/${section.course}/section/${section.id}/lesson/create`);
  };

  return (
    <div className="section">
      <div onClick={handleExpandClick} className="clickable">
        {section.title}
      </div>

      {isExpanded && (
        <React.Fragment>
          {isCreator && (
            <button className="text-red-500 font-medium  update-button" onClick={() => onUpdate()}>
              Update
            </button>
          )}

          {isCreator && (
            <button className="text-red-500 font-medium  create-button" onClick={() => handleCreateLesson()}>
              Create new lesson
            </button>
          )}

          <ul className="lesson-list">
            {section.lessons.map((lesson: Lesson, index: number) => (
              <li key={lesson.id} className="lesson-item">
                <Link href={`/course/${section.course}/section/${section.id}/lesson/${lesson.id}`}>
                  <span style={{color:'#57595F'}}>{`${index + 1}. ${lesson.title}`}</span>
                </Link>
              </li>
            ))}
          </ul>
        </React.Fragment>
      )}
    </div>
  );
};

export default Section;
