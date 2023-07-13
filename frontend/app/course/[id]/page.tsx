"use client"
import React, { Component, useContext, useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { StarIcon } from '@heroicons/react/24/solid'
import { getAuthorizedViewCourse } from "../../utils/getAllCourses.ts";
import { UserContext } from "../../layout.tsx";
import { useRouter, useSearchParams } from "next/navigation";
import Section from "@/app/components/section/page.tsx";
import './style.css'
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
          {course && (
            <>
            <div className="container">
              <h1 className='text-2xl font-bold pt-6 text-black title'>{course.title}</h1>
              <p className='text-base font-normal pt-6 opacity-75 description'>{course.description}</p>
              <p className=' font-medium price'>{course.price}</p>
              <div className='rating'>
                <StarIcon className="h-5 w-5 text-gold" />
                <span className='text-red text-22xl font-medium'>{course.rating}</span>
              </div>
              <button
                className='button'
                onClick={() => router.push(`/course/${params.id}/section/create`)}
              >
                Add New Section
              </button>
              {course.sections.map((section) => {
                return <Section section={section} />;
              })}
              </div>
            </>
          )}
        </>
      );

}