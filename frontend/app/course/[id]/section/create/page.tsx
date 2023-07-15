"use client";
import { useContext, useState } from "react";
import axios from "axios";
import { UserContext } from "@/app/layout.tsx";
import { useRouter } from "next/navigation";
import { getBaseURL } from "@/app/utils/getBaseURL";

type SectionForm = {
	title: string;
	course: string;
};

export default function Create({ params }: { params: { id: string } }) {
	const router = useRouter();
	const [form, setForm] = useState<SectionForm>({
		title: "",
		course: params.id,
	});
	const { isLoggingIn, setIsLoggingIn, setToken, token, userId } =
		useContext(UserContext)!;

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setForm({ ...form, [event.target.name]: event.target.value });
	};
	const handleSubmit = async () => {
		if (!form.title) {
			alert("No title added");
			return;
		}
		console.log("sssss", form);
		const url = `${getBaseURL()}/app/courses/create_section`;
		try {
			const response = await axios.post(
				url,
				{
					...form,
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
	return (
		<div className="form-style-8">
			<h2>Create a section</h2>
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
