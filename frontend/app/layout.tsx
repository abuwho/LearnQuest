"use client";
import "./globals.css";
import Navbar from "./components/Navbar/index";
import Footer from "./components/Footer/Footer";
import { useState, createContext, useEffect } from "react";
import axios from "axios";
import React from "react";
import { getBaseURL } from "./utils/getBaseURL";
import Banner from "./components/Banner/index";
import Courses from "./components/Courses/index";
import Companies from "./components/Companies/Companies";
import Mentor from "./components/Mentor/index";
import Testimonials from "./components/Testimonials/index";
import Newsletter from "./components/Newsletter/Newsletter";

type userIdType = {
	id: string;
	username: string;
	email: string;
};

const emtpyUserId = {
	id: "",
	username: "",
	email: "",
};
export const UserContext = createContext<{
	userId: userIdType | undefined;
	token: string;
	setToken: (token: string) => void;
	isLoggingIn: boolean;
	setIsLoggingIn: (isLoggingIn: boolean) => void;
} | null>(null);

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	const [userId, setUserId] = useState<userIdType>();
	const [token, setToken] = useState<string>("");
	const [isLoggingIn, setIsLoggingIn] = useState<boolean>(false);
	const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
	const userContextValue = {
		userId: userId,
		token: token,
		setToken: (newToken: string) => {
			localStorage.setItem("token", newToken);
			setToken(newToken);
		},
		isLoggingIn: isLoggingIn,
		setIsLoggingIn: setIsLoggingIn,
	};
	useEffect(() => {
		console.log("token", token);
	}, [token]);

	const connectAccount = async () => {
		if (!token || token === "") {
			setIsLoggedIn(false);
			try {
				localStorage.removeItem("token");
			} catch {}
			setUserId({
				id: "",
				username: "",
				email: "",
			});
			return;
		}
		try {
			const url = `${getBaseURL()}/auth/get_current_user/`
			const response = await axios.get(
				url,
				{
					headers: {
						Authorization: `Token ${token}`,
					},
				}
			);
			const user = response.data.user;
			setUserId({
				username: user.username,
				email: user.email,
				id: user.id,
			});
		} catch (e) {
			console.log(e, "userid");
			setIsLoggedIn(false);
			setUserId(emtpyUserId);
			localStorage.removeItem("token");
			return;
		}
	};

	useEffect(() => {
		const storedToken = localStorage.getItem("token");
		if (!storedToken) return;
		setToken(storedToken);
	}, []);
	useEffect(() => {
		localStorage.setItem("token", token);
		connectAccount();
	}, [token]);
	useEffect(() => {
		console.log("userId", userId);
	}, [userId]);
	return (
		<html lang="en">
			<UserContext.Provider value={userContextValue}>
				<body>
					<Navbar />
					{!token ? (
						<>
							<Banner />

							<Companies />

							<Courses />

							<Mentor />

							<Newsletter />

							<Testimonials />

							

						</>

					) : (
						<React.Fragment>{children}</React.Fragment>
					)}
					<Footer />
				</body>
			</UserContext.Provider>
		</html>
	);
}
