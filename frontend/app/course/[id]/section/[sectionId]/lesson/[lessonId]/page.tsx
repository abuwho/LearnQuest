"use client";
import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import { UserContext } from "@/app/layout.tsx";
import VideoViewer from "@/app/components/VideoViewer";
import "./lesson.css";
import { useRouter } from "next/navigation";
import dynamic from "next/dynamic";
import { getBaseURL } from "@/app/utils/getBaseURL";
import { getAuthorizedViewCourse, getCart } from "@/app/utils/getAllCourses";
import Spinner from "@/app/components/Spinner";

const PdfViewer = dynamic(() => import("@/app/components/PdfViewer"), {
	ssr: false,
});

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

const LessonPage = ({
	params: { sectionId, lessonId, id: courseId },
}: {
	params: {
		sectionId: string;
		lessonId: string;
		id: string;
	};
}) => {
	const router = useRouter();
	const [isCreator, setIsCreator] = useState(false)
	const { token, userId } = useContext(UserContext)!;
	const [lessonDetails, setLessonDetails] = useState<Lesson>();
	const [file, setFile] = useState<string>();
	const [videoLink, setVideoLink] = useState<string>();
	const getCourse = async () => {
		if (!token || !userId?.id) return;
		await new Promise((resolve) => setTimeout(resolve, 1000))
		const fetchedCourse = await getAuthorizedViewCourse(courseId, token);
		console.log(fetchedCourse);
		setIsCreator(fetchedCourse.instructor === userId.id)
	}
	useEffect(() => {
		const url = `${getBaseURL()}/app/courses/get_lessons_in_section/${sectionId}`;
		const fetchData = async () => {
			const response = await axios.get<IResponseGetLessons>(
				url,
				{
					// responseType: "arraybuffer",
					headers: {
						Authorization: `Token ${token}`,
						"Content-Type": "multipart/form-data",
					},
				}
			);

			const thisLesson = response.data.lessons.find(
				(lesson) => lessonId === lesson.id
			);

			if (!thisLesson) return;

			setLessonDetails(thisLesson);

			if (thisLesson.type === "pdf") {
				const blob = new Blob([thisLesson.pdf!], {
					type: "application/pdf",
				});
				setFile(URL.createObjectURL(blob));
			} else if (thisLesson.type === "link" || thisLesson.type === 'video') {
				setVideoLink(thisLesson.video_url!);
			}
		};

		fetchData();
	}, [lessonId, sectionId, token]);
	useEffect(() => {
		if (!token) return;
		getCourse();
	}, [token, userId]);

	const onUpdate = () => {
		router.push(
			`/course/${courseId}/section/${sectionId}/lesson/${lessonId}/update`
		);
	};

	if (!lessonDetails) return <Spinner/>;;

	return (
		<div className="container">
			<div className="buttons">
				{
					isCreator && (
					<button className="update-button" onClick={() => onUpdate()}>
						Update
					</button>
					)
				}
				{/* <button className="delete-button">Delete</button> */}
			</div>
			<div className="info">
				<h1>{lessonDetails.title}</h1>
			</div>
			{lessonDetails.type === "pdf" ? (
				<PdfViewer pdfFile={lessonDetails.pdf!} />
			) : (
				// <></>
				<React.Fragment>
					<VideoViewer videoLink={videoLink!} />
				</React.Fragment>
			)}
		</div>
	);
};

export default LessonPage;
