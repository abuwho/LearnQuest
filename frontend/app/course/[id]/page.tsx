"use client"
import React, { Component, useContext, useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { StarIcon } from '@heroicons/react/24/solid'
import { getAuthorizedViewCourse } from "../../utils/getAllCourses.ts";
import { UserContext } from "../../layout.tsx";
import { useRouter, useSearchParams } from "next/navigation";
import Section from "@/app/components/section/page.tsx";
export default function Course({ params }: { params: { id: string } }) {

    const [course, setCourse] = useState()
    const { isLoggingIn, setIsLoggingIn, setToken, token, userId } = useContext(UserContext)!
    const router = useRouter()
    const getCourse = async () => {
        if (!token || !userId?.id) return
        const fetchedCourse = (await getAuthorizedViewCourse(params.id, token))
        console.log('fetched course :', fetchedCourse)
        setCourse(fetchedCourse)
    }
    useEffect(() => {
        if (!token) return
        getCourse()
    }, [token, userId])
    return (
        <>
            { course && (<>
                <h1>

                {
                    course?.title
                }
            </h1>
            <h1>
                {course?.description}
            </h1>

            <h1>
                {course?.price}
            </h1>
            <h1>
                {course?.rating}
            </h1>
            <button
                onClick={() => router.push(`/course/${params.id}/section/create`)}
            >
                add new section
            </button>
            {
                course?.sections.map((section)=>
                {
                    return <Section section = {section}/>
                }
                )
            }
            </>
            )
            }
        </>
    )

}