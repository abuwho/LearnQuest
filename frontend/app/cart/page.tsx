"use client"
import React, { Component, useContext, useEffect, useState } from "react";

import { UserContext } from "../layout.tsx";
import { useRouter } from "next/navigation";
import { cartCheckout, getAllCreatedCourses, getCart, removeCourseFromCart } from "../utils/getAllCourses.ts";

export default function Course({ params }: { params: { id: string } }) {

    const [cart, setCart] = useState()
    const { isLoggingIn, setIsLoggingIn, setToken, token, userId } = useContext(UserContext)!
    const router = useRouter()
    const getUserCart = async () => {
        const response = await getCart(token)
        setCart(response)
    }

    useEffect(() => {
        if (!token) return
        getUserCart()
    }, [token, userId])

    const removeFromCart = async (courseId: string) => {
        await removeCourseFromCart(courseId, token)
        await getUserCart()
    }

    if (!cart) {
        return
    }
    return (
        <div>
            {cart.courses.map(course => {
                return <div className="flex justify-between pt-1">
                    <h3>{course.title}</h3>
                    <h3>{course.price}$</h3>
                    <button onClick={() => removeFromCart(course.id)}>remove from cart</button>
                </div>
            }
            )}
            <h3>total: {cart.total_price}$</h3>
            <button
                onClick={
                   async () => { 
                       const response = await cartCheckout(token)
                      if(response) router.push('/mycourses') 
                    }
                }
            >Checkout</button>
        </div >
    )

}