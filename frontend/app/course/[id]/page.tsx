"use client";
import React, { Component, useContext, useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { StarIcon } from "@heroicons/react/24/solid";
import { addCourseToCart, getAuthorizedViewCourse, getCart, isUserEnrolled, removeCourseFromCart } from "../../utils/getAllCourses.ts";
import { UserContext } from "../../layout.tsx";
import { useRouter, useSearchParams } from "next/navigation";
import Section from "@/app/components/section";
import axios from "axios";
import './style.css'
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

export default function Course({ params }: { params: { id: string } }) {
    const [course, setCourse] = useState();
    const [isCreator, setIsCreator] = useState(false)
    const [isEnrolled, setIsEnrolled] = useState(false)
    const [isInCart, setIsInCart] = useState<boolean>()
    const { isLoggingIn, setIsLoggingIn, setToken, token, userId } =
        useContext(UserContext)!;
    const router = useRouter();
    const getCourse = async () => {
        if (!token || !userId?.id) return;
        await new Promise((resolve) => setTimeout(resolve, 1000))
        const userCart = await getCart(token)
        const fetchedCourse = await getAuthorizedViewCourse(params.id, token);
        console.log(fetchedCourse);
        setIsCreator(fetchedCourse.instructor === userId.id)
        const updatedSections = await Promise.all(
            fetchedCourse.sections.map(async (curSection: any) => {
                try {
                    const response = await axios.get<IResponseGetLessons>(
                        `http://0.0.0.0:8080/app/courses/get_lessons_in_section/${curSection.id}`,
                        {
                            // responseType: "arraybuffer",
                            headers: {
                                Authorization: `Token ${token}`,
                                "Content-Type": "multipart/form-data",
                            },
                        }
                    );
                    return {
                        ...curSection,
                        lessons: response.data.lessons,
                    };
                }
                catch {
                    return {
                        ...curSection,
                        lessons: [],
                    };
                }
            })
        );

        console.log({ updatedSections });
        const t = (userCart.courses.map((e: { id: any; }) => e.id)).indexOf(params.id) !== -1
        setIsInCart(t)
        setCourse({
            ...fetchedCourse,
            sections: updatedSections,
        });
    };
    const checkIsEnrolled =async () => {
        setIsEnrolled(await isUserEnrolled(params.id,token))
    }
    useEffect(() => {
        if (!token) return;
        getCourse();
        checkIsEnrolled()
    }, [token, userId]);

    return (
        <>
            {course && (
                <>
                 <div className="containers">
                    <h1 className='text-2xl font-bold pt-6 text-black title'>{course?.title}</h1>
                    {
                        (!isInCart && !isCreator) && (
                            <button
                            className="cart-button"
                                onClick={() => { addCourseToCart(params.id, token) 
                                setIsInCart(true)}}
                            >
                                add to cart
                            </button>
                        )
                    }
                     {
                        (isInCart && !isCreator) && (
                            <button
                            className="cart-button"
                                onClick={() => { removeCourseFromCart(params.id, token) 
                                setIsInCart(false)}}
                            >
                                remove from cart
                            </button>
                        )
                    }
                    <p className='text-base font-normal pt-6 opacity-75 description'>{course?.description}</p>

                    <p className=' font-medium price'>{course?.price}$</p>
                    <div className='rating'>
                        <StarIcon className="h-5 w-5 text-gold" />
                        <span className='text-red text-22xl font-medium'>{course.rating}</span>
                    </div>
                   
                    {
                        isCreator &&
                        <button
                        className='text-red-500 font-medium  button'
                            onClick={() =>
                                router.push(`/course/${params.id}/section/create`)
                            }
                        >
                            add new section
                        </button>
                    }

                    {course.sections.map((section: any) => {
                        return <Section key={section.id} section={section} 
                            isAuthorized = {isCreator||isEnrolled}
                            isCreator = {isCreator}
                        />;
                    })}
                    </div>
                </>
            )}
        </>
    );
}
