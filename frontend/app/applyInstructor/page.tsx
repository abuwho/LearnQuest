"use client";
import axios from "axios";
import { useContext, useState } from "react";
import "./styles.css";
import { UserContext } from "../layout.tsx";
import { useRouter } from "next/navigation";
import { getBaseURL } from "../utils/getBaseURL.ts";

const RequestToInstructPage = () => {
	const router = useRouter();
	const { token } = useContext(UserContext)!;

	const [reason, setReason] = useState("");

	const handleSubmit = async () => {
		try {
			const url = `${getBaseURL()}/app/apply/`
			await axios.post(
				url,
				{ reason },
				{
					headers: {
						Authorization: `Token ${token}`,
					},
				}
			);
		} catch {
			// todo: Laith implement the toast
		}
		router.push("/");
	};

	return (
		<div className="form-style-8">
			<h2>Apply to be an instructor</h2>
			<form action="">
				<input
					type="text"
					name="reason"
					placeholder="Why do you think you're a good fit?"
					value={reason}
					onChange={(e) => {
						setReason(e.target.value);
					}}
				/>
				{/* <input type="text" name="description" placeholder='Description' value={form.description} onChange={handleInputChange} />
                <input type="number" name="price" placeholder="Price" value={form.price} onChange={handleInputChange} /> */}
				<input
					type="button"
					value="Submit"
					onClick={() => handleSubmit()}
				/>
			</form>
		</div>
	);
};



export default RequestToInstructPage;
