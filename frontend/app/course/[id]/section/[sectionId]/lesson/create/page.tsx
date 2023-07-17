"use client";
import { UserContext } from "@/app/layout.tsx";
import axios from "axios";
import { ChangeEvent, useContext, useState } from "react";
import "./styles.css";
import { useRouter } from "next/navigation";
import { getBaseURL } from "@/app/utils/getBaseURL";

const CreateLesson = ({
	params,
}: {
	params: { sectionId: string; id: string; lessonId: string };
}) => {
	const router = useRouter();
	const { token } = useContext(UserContext)!;
	const [title, setTitle] = useState("");
	const [type, setType] = useState("link");
	const [videoLink, setVideoLink] = useState("");
	const [summary, setSummary] = useState("");

	const [selectedFile, setSelectedFile] = useState<File | null>(null);

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files?.[0];
		if (!file) return;
		setSelectedFile(file);
	};

	const handleSubmit = async () => {
		const url = `${getBaseURL()}/app/courses/create_lesson`;
		try {
			if (type === "link" && !videoLink) return;
			if (type === "pdf" && !selectedFile) return;

			const videoOrPdf =
				type === "link"
					? { video_url: videoLink }
					: { pdf: selectedFile };
			await axios.post(
				url,
				{
					title,
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
				`/course/${params.id}}`
			);
		} catch {
			// todo: Laith implement the toast
		}
	};

	return (
		<div className="form-style-8">
			<h2>Create your own lesson</h2>
			<form action="">
				<label htmlFor="title">Lesson name:</label>
				<input
					id="title"
					type="text"
					name="title"
					placeholder="The best lesson"
					value={title}
					onChange={(e) => setTitle(e.target.value)}
				/>

				<label htmlFor="summary">Lesson summary:</label>
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
					<option value="link">Video</option>
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
					value="Upload your lesson!"
					onClick={() => handleSubmit()}
				/>
			</form>
		</div>
	);
};

export default CreateLesson;
