"use client";
import { UserContext } from "@/app/layout.tsx";
import axios from "axios";
import { ChangeEvent, useContext, useEffect, useState } from "react";
import "./updateLesson.css";
import Spinner from "@/app/components/Spinner";
import { useRouter } from "next/navigation";
import { getBaseURL } from "@/app/utils/getBaseURL";

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

const UpdateLesson = ({
	params,
}: {
	params: { sectionId: string; lessonId: string; id: string };
}) => {
	const router = useRouter();
	const { token } = useContext(UserContext)!;
	const [title, setTitle] = useState("");
	const [type, setType] = useState("video");
	const [videoLink, setVideoLink] = useState("");
	const [summary, setSummary] = useState("");
	const [file, setFile] = useState<string>();
	const [didFetch, setDidFetch] = useState<boolean>();

	const [selectedFile, setSelectedFile] = useState<File | null>(null);

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files?.[0];
		if (!file) return;
		setSelectedFile(file);
	};

	useEffect(() => {
		const url = `${getBaseURL()}/app/courses/get_lessons_in_section/${params.sectionId}`;
		if (!token) return;
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
				(lesson) => params.lessonId === lesson.id
			);

			if (!thisLesson) return;

			setSummary(thisLesson.summary);
			setTitle(thisLesson.title);
			setTitle(thisLesson.type);
			if (thisLesson.type === "pdf") {
				setFile(thisLesson.pdf!);
			} else {
				setVideoLink(thisLesson.video_url!);
			}
			setDidFetch(true);
		};

		fetchData();
	}, [params.lessonId, params.sectionId, token]);

	const handleSubmit = async () => {
		const url = `${getBaseURL()}/app/courses/update_lesson`;
		try {
			if (type === "video" && !videoLink) return;
			if (type === "pdf" && !selectedFile) return;

			const videoOrPdf =
				type === "video"
					? { video_url: videoLink }
					: { pdf: selectedFile };

			await axios.put(
				url,
				{
					title,
					id: params.lessonId,
					section: params.sectionId,
					type,
					summary,
					...videoOrPdf,
				},
				{
					headers: {
						Authorization: `Token ${token}`,
						"Content-Type": "multipart/form-data",
					},
				}
			);
			router.push(
				`/course/${params.id}/section/${params.sectionId}/lesson/${params.lessonId}`
			);
		} catch {
			// todo: Laith implement the toast
		}
	};

	if (!didFetch) return <Spinner />;

	return (
		<div className="form-style-8">
			<h2>Update your lesson</h2>
			<form action="">
				<label htmlFor="title">Lesson new name:</label>
				<input
					id="title"
					type="text"
					name="title"
					placeholder="The best lesson"
					value={title}
					onChange={(e) => setTitle(e.target.value)}
				/>

				<label htmlFor="summary">Lesson new summary:</label>
				<input
					id="summary"
					type="text"
					name="summary"
					placeholder="The best lesson's summary"
					value={summary}
					onChange={(e) => setSummary(e.target.value)}
				/>

				<label htmlFor="options">Lesson type:</label>
				<select
					id="options"
					value={type}
					onChange={(e) => setType(e.target.value)}
				>
					<option value="video">Video</option>
					<option value="pdf">PDF file</option>
				</select>

				{type === "pdf" ? (
					<>
						<label htmlFor="pdfFile">Select a PDF file:</label>
						<input
							type="file"
							id="pdfFile"
							accept=".pdf"
							onChange={handleFileChange}
						/>
					</>
				) : (
					<>
						<label htmlFor="videoLink">Type the video link:</label>
						<input
							id="videoLink"
							type="url"
							name="link"
							placeholder="video link"
							value={videoLink}
							onChange={(e) => setVideoLink(e.target.value)}
						/>
					</>
				)}

				<input
					type="button"
					value="Update your lesson!"
					onClick={() => handleSubmit()}
				/>
			</form>
		</div>
	);
};

export default UpdateLesson;
