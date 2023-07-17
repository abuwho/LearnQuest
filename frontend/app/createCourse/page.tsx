"use client"
import { useState, FormEvent, useEffect, useContext } from 'react';
import { Box, FormControl, FormLabel, Input, Button, FormErrorMessage, Stack, useToast } from "@chakra-ui/react";
import objectToFormData from '../utils/objectToFormData';
import './createCourse.css'
import { getBaseURL } from '../utils/getBaseURL';
import { UserContext } from '../layout.tsx';
import { useRouter } from 'next/navigation';

type CourseForm = {
    title: string;
    description: string;
    price: number;
};

const initialFormState: CourseForm = {
    title: '',
    description: '',
    price: 0
};

export default function CreateCourse() {
    const [form, setForm] = useState<CourseForm>(initialFormState);
    const { isLoggingIn, setIsLoggingIn, setToken, token, userId } = useContext(UserContext)!
    const router = useRouter()

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [event.target.name]: event.target.value });
    };

    const validateForm = () => {
        if (!form.title) {
            return true
        }
        return false
    };

    const handleSubmit = async () => {
        console.log(form)
        if (validateForm()) {
            return
        }
        if (token === null) {
            router.push('/')
           return
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
               alert('created!')
                // Then reset the form
                router.push('/mycourses')
                setForm(initialFormState);
                
            }
        } catch (error) {
            console.error('An error occurred while submitting the form:', error);
            return
        }
    };

    return (
        <div className='form-style-8'>
            <h2>Create a course</h2>
            <form action="">
                <input type="text" name="title" placeholder="Course title:" value={form.title} onChange={handleInputChange} />
                <input type="text" name="description" placeholder='Description' value={form.description} onChange={handleInputChange} />
                <input type="number" name="price" placeholder="Price" value={form.price} onChange={handleInputChange} />
                <input type="button" value="Submit" onClick={() => handleSubmit()} />
            </form>
        </div>
    );
}
