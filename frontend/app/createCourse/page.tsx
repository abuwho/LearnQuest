"use client"
import { useState, FormEvent, useEffect } from 'react';
import { Box, FormControl, FormLabel, Input, Button, FormErrorMessage, Stack, useToast } from "@chakra-ui/react";
import objectToFormData from '../utils/objectToFormData';

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
    const [errors, setErrors] = useState<CourseForm>(initialFormState);
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
        try {
            const response = await fetch('http://0.0.0.0:8080/app/courses/create', {
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
        <>
            <h1>Create a Course</h1>
                    <FormLabel >Course title:</FormLabel>
                    <input type="text" name="title" onChange={handleInputChange} />

                    <form >Course Description:</form>
                    <input type="text" name="description" value={form.description} onChange={handleInputChange} />
           
                    <form >Course Price:</form>
                    <input type="number" name="price" value={form.price} onChange={handleInputChange} />
           
                <button type="submit" onClick={()=>handleSubmit()}>Submit</button>
       </>
    );
}
