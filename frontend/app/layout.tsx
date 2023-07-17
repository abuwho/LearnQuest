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

type walletType = {
	id: string;
	currncy: string;
	balance: number;
};


const emtpyUserId = {
	id: "",
	username: "",
	email: "",
};
export const UserContext = createContext<{
	userId: userIdType | undefined;
	wallet: walletType;
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
	const [wallet, setWallet] = useState<walletType>();
	const userContextValue = {
		userId: userId,
		token: token,
		setToken: (newToken: string) => {
			localStorage.setItem("token", newToken);
			setToken(newToken);
		},
		isLoggingIn: isLoggingIn,
		setIsLoggingIn: setIsLoggingIn,
		wallet: wallet,
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
			const wallet = response.data.wallet;
			setUserId({
				username: user.username,
				email: user.email,
				id: user.id,
			});

			setWallet({
				id: wallet.id,
				currncy: wallet.currency,
				balance: wallet.balance,
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

	useEffect(() => {
		connectAccount();
	}, [wallet]);

	return (
		<html lang="en">
			<UserContext.Provider value={userContextValue}>
				<body>
					<Navbar />
					{!token ? (
						<>
							<link rel="icon" href="/learnquest_favicon.ico" type="image/x-icon" sizes="any"></link>
							<title> LearnQuest </title>
							<Banner />

							<Companies />

							<Courses />

							<Mentor />

							<Newsletter />

							<Testimonials />

							

						</>

					) : (
						<>
						<link rel="icon" href="/learnquest_favicon.ico" type="image/x-icon" sizes="any"></link>
							<title> LearnQuest </title>
							<React.Fragment>
								{children}
							</React.Fragment>
						</>
						
					)}
					<Footer />
				</body>
			</UserContext.Provider>
		</html>
	);
}
