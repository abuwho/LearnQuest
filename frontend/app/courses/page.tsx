"use client";
import React, { useContext, useEffect, useState } from "react";
import Image from "next/image";
import { StarIcon } from "@heroicons/react/24/solid";
import { UserContext } from "../layout.tsx";
import { useRouter } from "next/navigation";

// CAROUSEL DATA

interface DataType {
	heading: string;
	heading2: string;
	imgSrc: string;
	name: string;
	students: number;
	classes: number;
	price: number;
	rating: number;
}

const postData: DataType[] = [
	{
		heading: "Full stack modern",
		heading2: "javascript",
		name: "Colt stelle",
		imgSrc: "/assets/courses/courseone.png",
		students: 150,
		classes: 12,
		price: 20,
		rating: 4.7,
	},
	{
		heading: "Design system",
		heading2: "with React programme",
		name: "Colt stelle",
		imgSrc: "/assets/courses/coursetwo.png",
		students: 130,
		classes: 12,
		price: 20,
		rating: 4.7,
	},
	{
		heading: "Design banner",
		heading2: "with Figma",
		name: "Colt stelle",
		imgSrc: "/assets/courses/coursethree.png",
		students: 120,
		classes: 12,
		price: 20,
		rating: 4.7,
	},
	{
		heading: "We Launch Delia",
		heading2: "Webflow this Week!",
		name: "Colt stelle",
		imgSrc: "/assets/courses/courseone.png",
		students: 150,
		classes: 12,
		price: 20,
		rating: 4.7,
	},
	{
		heading: "We Launch Delia",
		heading2: "Webflow this Week!",
		name: "Colt stelle",
		imgSrc: "/assets/courses/coursetwo.png",
		students: 150,
		classes: 12,
		price: 20,
		rating: 4.7,
	},
	{
		heading: "We Launch Delia",
		heading2: "Webflow this Week!",
		name: "Colt stelle",
		imgSrc: "/assets/courses/coursethree.png",
		students: 150,
		classes: 12,
		price: 20,
		rating: 4.7,
	},
];

// CAROUSEL SETTINGS

export default function MultipleItems() {
	type Course = {
		id: string;
		instructor: string;
		description: string;
		rating: string;
		title: string;
		price: string;
		image: string;
		students: string[];
	};
	const { isLoggingIn, setIsLoggingIn, setToken, token, userId } =
		useContext(UserContext)!;
	const router = useRouter();
	const [courses, setCourses] = useState<Course[]>([]);
	useEffect(() => {
		const fetchCourses = async () => {
			const data = await fetch("http://127.0.0.1:8080/app/courses/");
			let parsed = await data.json();
			setCourses(parsed);
		};
		fetchCourses();
	}, []);
	useEffect(() => {
		if (!courses) return;
		console.log("ahhhhhhhh", courses);
	}, [courses]);
	const settings = {
		dots: false,
		infinite: true,
		slidesToShow: 3,
		// centerMode: true,
		slidesToScroll: 2,
		arrows: false,
		autoplay: false,
		speed: 500,
		cssEase: "linear",
		responsive: [
			{
				breakpoint: 1200,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 1,
					infinite: true,
					dots: false,
				},
			},
			{
				breakpoint: 600,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
					infinite: true,
					dots: false,
				},
			},
		],
	};

	const handleViewClick = async (id: string) => {
		// const course = await getAuthorizedViewCourse(id, token)/
		router.push(`/course/${id}`);
	};

    if(!courses.length){
        return <></>
    }
    return (
        <div id="courses">
            <div className='mx-auto max-w-7xl sm:py-8 px-4 lg:px-8 '>

                <div className="sm:flex justify-between items-center">
                    <h3 className="text-midnightblue text-4xl lg:text-55xl font-semibold mb-5 sm:mb-0">All courses.</h3>
                </div>
                        {courses.map((items, i) => {
                            return(
                            <div key={items.id}>

                                <div className='bg-white m-3 px-3 pt-3 pb-12 my-20 shadow-courses rounded-2xl'>
                                    <div className="relative rounded-3xl">
                                        <Image src={items.image} alt="gaby" width={389} height={262} className="m-auto clipPath" />
                                        <div className="absolute right-5 -bottom-2 bg-ultramarine rounded-full p-6">
                                            <h3 className="text-white uppercase text-center text-sm font-medium">best <br /> seller</h3>
                                        </div>
                                    </div>

								<div className="px-3">
									<h4 className="text-2xl font-bold pt-6 text-black">
										{items.title}
									</h4>

									<div className="flex justify-between items-center py-6">
										<div className="flex gap-4">
											<h3 className="text-red text-22xl font-medium">
												{items.rating}
											</h3>
											<div className="flex">
												<StarIcon className="h-5 w-5 text-gold" />
												<StarIcon className="h-5 w-5 text-gold" />
												<StarIcon className="h-5 w-5 text-gold" />
												<StarIcon className="h-5 w-5 text-gold" />
												<StarIcon className="h-5 w-5 text-gold" />
											</div>
										</div>
										<div>
											<h3 className="text-3xl font-medium">
												${items.price}
											</h3>
										</div>
									</div>

									<hr style={{ color: "#C4C4C4" }} />

									<div>
										<button
											type="submit"
											onClick={() =>
												handleViewClick(items.id)
											}
											className="bg-white w-full text-Blueviolet border border-semiblueviolet font-medium py-2 px-4 rounded"
										>
											view course
										</button>
									</div>

									<hr style={{ color: "#C4C4C4" }} />
									{/* <div className="flex justify-between pt-6">
                                            <div>
                                            <button type="submit" onClick={() => handleViewClick(items.id)} className="bg-white w-full text-Blueviolet border border-semiblueviolet font-medium py-2 px-4 rounded">
                                                    view course
                                                </button>
                                            </div>
                                            <div>
                                            <button type="submit" onClick={() => handleEditClick(items.id)} className="bg-white w-full text-Blueviolet border border-semiblueviolet font-medium py-2 px-4 rounded">
                                                    edit course
                                                </button>
                                            </div>
                                            <div>
                                            <button type="submit" onClick={() => handleDeleteClick(items.id)} className="bg-white w-full text-Blueviolet border border-semiblueviolet font-medium py-2 px-4 rounded">
                                                    delete course
                                                </button>
                                            </div>
                                        </div> */}
                                    </div>
                                </div>
                            </div>
                        )})}
            </div>
        </div>

    )
							
}
