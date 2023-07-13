"use client"
import Slider from "react-slick";
import React, { Component, useContext, useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { StarIcon } from '@heroicons/react/24/solid'
import { get } from "http";
import {getAllCreatedCourses} from "../utils/getAllCourses";
import { UserContext } from "../layout.tsx";
export default function Mycourses() {

    // const [token, setToken] = useState<string | null>()
    const [courses, setCourses] = useState<any[]>([])

    const {isLoggingIn,setIsLoggingIn, setToken,token,userId}= useContext(UserContext)!
    const getCourses = async() => {
        if(!token || !userId?.id) return
        
        const fetchedCourses = (await getAllCreatedCourses(token)).filter((course)=> {return course.instructor===userId.id})
        console.log('courses for user',fetchedCourses)
        setCourses(fetchedCourses)
    }
    useEffect(() => {
        if(!token) return
        getCourses()
    }, [token,userId])

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
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: false
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: false
                }
            }
        ]
    };
    return (
        <div id="courses">
            <div className='mx-auto max-w-7xl sm:py-8 px-4 lg:px-8 '>

                <div className="sm:flex justify-between items-center">
                    <h3 className="text-midnightblue text-4xl lg:text-55xl font-semibold mb-5 sm:mb-0">My courses.</h3>
                </div>


                <Slider {...settings}>
                        {courses.map((items, i) => (
                            <div key={i}>

                                <div className='bg-white m-3 px-3 pt-3 pb-12 my-20 shadow-courses rounded-2xl'>
                                    <div className="relative rounded-3xl">
                                        <Image src={items.imgSrc} alt="gaby" width={389} height={262} className="m-auto clipPath" />
                                        <div className="absolute right-5 -bottom-2 bg-ultramarine rounded-full p-6">
                                            <h3 className="text-white uppercase text-center text-sm font-medium">best <br /> seller</h3>
                                        </div>
                                    </div>

                                    <div className="px-3">
                                        <h4 className='text-2xl font-bold pt-6 text-black'>{items.title}</h4>

                                        <div className="flex justify-between items-center py-6">
                                            <div className="flex gap-4">
                                                <h3 className="text-red text-22xl font-medium">{items.rating}</h3>
                                                <div className="flex">

                                                    <StarIcon className="h-5 w-5 text-gold" />
                                                    <StarIcon className="h-5 w-5 text-gold" />
                                                    <StarIcon className="h-5 w-5 text-gold" />
                                                    <StarIcon className="h-5 w-5 text-gold" />
                                                    <StarIcon className="h-5 w-5 text-gold" />
                                                </div>
                                            </div>
                                            <div>
                                                <h3 className="text-3xl font-medium">${items.price}</h3>
                                            </div>
                                        </div>

                                        <hr style={{ color: "#C4C4C4" }} />

                                        <div className="flex justify-between pt-6">
                                            <div className="flex gap-4">
                                                <Image src={'/assets/courses/book-open.svg'} alt="users" width={24} height={24} className="inline-block m-auto" />
                                                <h3 className="text-base font-medium text-black opacity-75">{items.sections.length} Sections</h3>
                                            </div>
                                            <div className="flex gap-4">
                                                <Image src={'/assets/courses/users.svg'} alt="users" width={24} height={24} className="inline-block m-auto" />
                                                <h3 className="text-base font-medium text-black opacity-75">{items.students.length} students</h3>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </Slider>
            </div>
        </div>

    )
}