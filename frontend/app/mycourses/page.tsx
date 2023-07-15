"use client";
import Slider from "react-slick";
import React, { Component, useContext, useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { StarIcon } from '@heroicons/react/24/solid'
import { get } from "http";
import { getAllCreatedCourses, getAuthorizedViewCourse, getEnrolledCourses } from "../utils/getAllCourses";
import { deleteCourse } from "../utils/deleteCourse.ts";
import { UserContext } from "../layout.tsx";
import { useRouter } from 'next/navigation';

export default function Mycourses() {
    const router = useRouter()
    // const [token, setToken] = useState<string | null>()
    const [courses, setCourses] = useState<any[]>([])
    const [enrolled, setEnrolled] = useState<any[]>([])
    const { isLoggingIn, setIsLoggingIn, setToken, token, userId } = useContext(UserContext)!
    const getCourses = async () => {
        if (!token || !userId?.id) return
        const enrolledCourses = (await getEnrolledCourses(token)).filter((course: { instructor: string; }) => { return course.instructor === userId.id })
        const fetchedCourses = (await getAllCreatedCourses(token)).filter((course: { instructor: string; }) => { return course.instructor === userId.id })
        setCourses(fetchedCourses)
        setEnrolled(enrolledCourses)
    }

    const handleViewClick = async (id: string) => {
        // const course = await getAuthorizedViewCourse(id, token)
        router.push(`/course/${id}`)
    }

    const handleEditClick = async (id: string) => {
        router.push(`/course/${id}/edit`)
    }

    const handleDeleteClick = async (id: string) => {
        await deleteCourse(id, token)
        window.location.reload()
    }

    useEffect(() => {
        if (!token) return
        getCourses()
    }, [token, userId])

    const renderCourses = (courses: any[]) => {
        if (courses.length === 0) {
            return null;
        }

        const coursesGroups = [];
        for (let i = 0; i < courses.length; i += 3) {
            const coursesGroup = courses.slice(i, i + 3);
            coursesGroups.push(coursesGroup);
        }

        return (
            <div>
                {coursesGroups.map((group, index) => (
                    <div className="flex justify-between space-x-4" key={index}>
                        {group.map((items) => (
                            <div className="w-full sm:w-1/3" key={items.id}>
                                <div className='bg-white m-3 px-3 pt-3 pb-12 my-20 shadow-courses rounded-2xl'>
                                    <div className="relative rounded-3xl">
                                        <Image src='/assets/courses/coursethree.png' alt="gaby" width={389} height={262} className="m-auto clipPath" />
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

                                        <div className="flex justify-between pt-6" style={{ marginBottom: '19px' }}>
                                            <div className="flex gap-4">
                                                <Image src={'/assets/courses/book-open.svg'} alt="users" width={24} height={24} className="inline-block m-auto" />
                                                <h3 className="text-base font-medium text-black opacity-75">{items.sections.length} Sections</h3>
                                            </div>
                                            <div className="flex gap-4">
                                                <Image src={'/assets/courses/users.svg'} alt="users" width={24} height={24} className="inline-block m-auto" />
                                                <h3 className="text-base font-medium text-black opacity-75">{items.students.length} students</h3>
                                            </div>
                                        </div>
                                        <hr style={{ color: "#C4C4C4" }} />
                                        <div className="flex justify-between pt-6">
                                            <div>
                                                <button style={{ color: '#3B82F6' }} type="submit" onClick={() => handleViewClick(items.id)} className="bg-white w-full text-Blueviolet border border-semiblueviolet font-medium py-2 px-4 rounded">
                                                    view course
                                                </button>
                                            </div>
                                            <div>
                                                <button style={{ color: '#3B82F6' }} type="submit" onClick={() => handleEditClick(items.id)} className="bg-white w-full text-Blueviolet border border-semiblueviolet font-medium py-2 px-4 rounded">
                                                    edit course
                                                </button>
                                            </div>
                                            <div>
                                                <button style={{ color: '#3B82F6' }} type="submit" onClick={() => handleDeleteClick(items.id)} className="bg-white w-full text-Blueviolet border border-semiblueviolet font-medium py-2 px-4 rounded">
                                                    delete course
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div id="courses">
            {renderCourses(courses) && (
                <div className='mx-auto max-w-7xl sm:py-8 px-4 lg:px-8 '>
                    <div className="sm:flex justify-between items-center">
                        <h3 className="text-midnightblue text-4xl lg:text-55xl font-semibold mb-5 sm:mb-0">Created Courses.</h3>
                    </div>
                    {renderCourses(courses)}
                </div>
            )}

            {renderCourses(enrolled) && (
                <div className='mx-auto max-w-7xl sm:py-8 px-4 lg:px-8 '>
                    <div className="sm:flex justify-between items-center">
                        <h3 className="text-midnightblue text-4xl lg:text-55xl font-semibold mb-5 sm:mb-0">Enrolled courses.</h3>
                    </div>
                    {renderCourses(enrolled)}
                </div>
            )}
        </div >
    )
}
