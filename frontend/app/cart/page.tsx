"use client";
import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../layout.tsx";
import { useRouter } from "next/navigation";
import { cartCheckout, getAllCreatedCourses, getCart, removeCourseFromCart } from "../utils/getAllCourses.ts";
import "./style.css";

export default function Course({ params }: { params: { id: string } }) {
  const [cart, setCart] = useState<any>();
  const { isLoggingIn, setIsLoggingIn, setToken, token, userId } = useContext(UserContext)!;
  const router = useRouter();

  const getUserCart = async () => {
    const response = await getCart(token);
    setCart(response);
  };

  useEffect(() => {
    if (!token) return;
    getUserCart();
  }, [token, userId]);

  const removeFromCart = async (courseId: string) => {
    await removeCourseFromCart(courseId, token);
    await getUserCart();
  };

  const handleCheckout = async () => {
    const response = await cartCheckout(token);
    if (response) router.push("/mycourses");
  };

  if (!cart) {
    return null;
  }

  return (
    <div className="containers">
      <div className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-semibold mb-4">Your Cart</h2>

        <div className="mb-8">
          {cart.courses.map((course: any) => (
            <div className="flex items-center justify-between py-2" key={course.id}>
              <div>
                <h3 className="text-xl">{course.title}</h3>
                <p className="text-gray-500">${course.price}</p>
              </div>
              <button
                onClick={() => removeFromCart(course.id)}
                className="text-red-500 font-medium button"
                
              >
                Remove
              </button>
            </div>
          ))}
        </div>

        <div className="flex items-center justify-between py-2">
          <h3 className="text-lg font-medium">Total:</h3>
          <h3 className="text-lg">${cart.total_price}</h3>
        </div>

        <button
          onClick={handleCheckout}
          className="text-red-500 font-medium  button"
        >
          Checkout
        </button>
      </div>
    </div>
  );
}
