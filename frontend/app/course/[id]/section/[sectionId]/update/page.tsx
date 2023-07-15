"use client";
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { UserContext } from "@/app/layout.tsx";
import "./styles.css";
import Spinner from "@/app/components/Spinner";
import { useRouter } from "next/navigation";

type SectionForm = {
	title: string;
	course: string;
};

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

export default function Create({
	params,
}: {
	params: { sectionId: string; lessonId: string; id: string };
}) {
	const router = useRouter();
	const [form, setForm] = useState<SectionForm>({
		title: "",
		course: params.id,
	});
	const [didFetch, setDidFetch] = useState<boolean>();

	const { isLoggingIn, setIsLoggingIn, setToken, token, userId } =
		useContext(UserContext)!;

	useEffect(() => {
		if (!token) return;
		const fetchData = async () => {
			const response = await axios.get<IResponseGetLessons>(
				`http://0.0.0.0:8080/app/courses/get_lessons_in_section/${params.sectionId}`,
				{
					// responseType: "arraybuffer",
					headers: {
						Authorization: `Token ${token}`,
						"Content-Type": "multipart/form-data",
					},
				}
			);

			setForm((oldForm) => ({ ...oldForm, title: response.data.title }));
			setDidFetch(true);
		};

		fetchData();
	}, [params.sectionId, token]);

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setForm({ ...form, [event.target.name]: event.target.value });
	};

	const handleSubmit = async () => {
		if (!form.title) {
			alert("No title added");
			return;
		}
		console.log("sssss", form);
		try {
			const response = await axios.put(
				"http://0.0.0.0:8080/app/courses/update_section",
				{
					title: form.title,
					section: params.sectionId,
				},
				{
					headers: {
						Authorization: `Token ${token}`, // Assuming `token` is in the scope
					},
				}
			);
			router.push(`/course/${params.id}`);
		} catch (e) {
			alert("cannot create section");
		}
	};

	if (!didFetch) return <Spinner />;

	return (
		<div className="form-style-8">
			<h2>Update the section</h2>
			<form action="">
				<input
					type="text"
					name="title"
					placeholder="Title:"
					value={form.title}
					onChange={handleInputChange}
				/>
				<input
					type="button"
					value="Submit"
					onClick={() => handleSubmit()}
				/>
			</form>
		</div>
	);
}
