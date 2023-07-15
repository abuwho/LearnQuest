"use client"
import { useState, FormEvent, useEffect } from 'react';
import { Box, FormControl, FormLabel, Input, Button, FormErrorMessage, Stack, useToast } from "@chakra-ui/react";
import objectToFormData from '../utils/objectToFormData';
import './createCourse.css'
import { getBaseURL } from '../utils/getBaseURL';

type CourseForm = {
    title: string;
    description: string;
    price: number |null;
};

const initialFormState: CourseForm = {
    title: '',
    description: '',
    price:null
};

export default function CreateCourse() {
    const [form, setForm] = useState<CourseForm>(initialFormState);
    const [token, setToken] = useState<string | null>()
    const toast = useToast();
    useEffect(()=>{
        if(!window) return
        setToken(localStorage.getItem('token'))
    },[])
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [event.target.name]: event.target.value });
    };

    const validateForm = () => {
        if (!form.title) {
        toast({
            title: "An error occurred.",
            description: "title cannot be empty",
            status: "error",
            duration: 3000,
            isClosable: true,
        });return true}
        if (form.price<0) { toast({
            title: "An error occurred.",
            description: "price is less than 0",
            status: "error",
            duration: 3000,
            isClosable: true,
        });return true}
        return false
    };

    const handleSubmit = async () => {
        console.log(form)
        if(validateForm()){
            return
        }
        if(token===null){
            toast({
                title: "Sign in to create a course",
                description: "Your course could not be created.",
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        }

        // If no errors, we can submit the form
        const url = `${getBaseURL()}/app/courses/create`
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    // 'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
                },
                body: JSON.stringify(form)

            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            } else {
                toast({
                    title: "Course Created.",
                    description: "Your course was successfully created.",
                    status: "success",
                    duration: 3000,
                    isClosable: true,
                });

                // Then reset the form
                setForm(initialFormState);
            }
        } catch (error) {
            console.error('An error occurred while submitting the form:', error);
            toast({
                title: "An error occurred.",
                description: "Your course could not be created.",
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        }
    };

    return (
        <div className='form-style-8'>
            <h2>Create a course</h2>
            <form action="">
                <input type="text" name="title" placeholder="Course title:" value = {form.title} onChange={handleInputChange} />
                <input type="text" name="description" placeholder='Description' value={form.description} onChange={handleInputChange} />
                <input type="number" name="price" placeholder="Price" value={form.price} onChange={handleInputChange} />
                <input  type="button" value="Submit"  onClick={()=>handleSubmit()}/>
            </form>
        </div>
    );
}
