"use client"
import { useState, FormEvent, useEffect, useContext } from 'react';
import './createCourse.css'
import { UserContext } from '@/app/layout.tsx';
import { getAuthorizedViewCourse } from '@/app/utils/getAllCourses';
import { useRouter } from 'next/navigation';
import { getBaseURL } from '@/app/utils/getBaseURL';
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

export default function EditCourse({ params }: { params: { id: string } }) {
    const [form, setForm] = useState<CourseForm>(initialFormState);
    const { isLoggingIn, setIsLoggingIn, setToken, token, userId } = useContext(UserContext)!
    const [course, setCourse] = useState()
    const router = useRouter()

    const getCourse = async () => {
        if (!token || !userId?.id) return
        const fetchedCourse = (await getAuthorizedViewCourse(params.id, token))
        console.log('fetched course :', fetchedCourse)
        setForm(fetchedCourse)
    }
    useEffect(() => {
        if (!token) return
        getCourse()
    }, [token, userId])

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
            return
        }
        // If no errors, we can submit the form
        try {
            const response = await fetch(`${getBaseURL()}/app/courses/${params.id}/update`, {
                method: 'PUT',
                headers: {
                    // 'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
                },
                body: JSON.stringify(form)

            });

            if (!response.ok) {
                alert('error')
                return
                // throw new Error(`HTTP error! status: ${response.status}`);
            } else {


                // Then reset the form
                setForm(initialFormState)
                router.push('/mycourses')
            }
        } catch (error) {
            console.error('An error occurred while submitting the form:', error);
            alert('error')
        };

    }

    return (
        <div className='form-style-8'>
            <h2>Edit course</h2>
            <form action="">
                <input type="text" name="title" placeholder="Course title:" value={form.title} onChange={handleInputChange} />
                <input type="text" name="description" placeholder='Description' value={form.description} onChange={handleInputChange} />
                <input type="number" name="price" placeholder="Price" value={form.price} onChange={handleInputChange} />
                <input type="button" value="Submit" onClick={() => handleSubmit()} />
            </form>
        </div>
    );
}