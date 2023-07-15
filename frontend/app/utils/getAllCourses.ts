import axios from 'axios'
export async function getAllCreatedCourses(token: string) {
    try {
        const response = (await fetch('http://0.0.0.0:8080/app/courses/created', {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            }
        }))

        if (!response.ok) {
            console.log('error', response)
            alert('request failed')
        } else {
            return await response.json()
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }
}
export async function getAuthorizedViewCourse(courseId: string, token: string) {
    try {
        const response = await axios.get(`http://0.0.0.0:8080/app/courses/${courseId}/preview`, {
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            },
        })
        console.log('jjjjjj', response)
        if (!response.data) {
            console.log('error', response)
            alert('request failed')
        } else {
            return response.data
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }
}
export async function getCart(token: string) {
    console.log('wwwwwwwww',token)
    try {
        const response = await axios.get(`http://0.0.0.0:8080/app/cart/get`, {
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            },
        })
        console.log('jjjjjj', response.data)
        if (!response.data) {
            console.log('error', response)
            alert('request failed')
        } else {
            return response.data
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }
}
export async function addCourseToCart(courseId: string, token: string) {
    try {
        const response = await axios.post(`http://0.0.0.0:8080/app/cart/add`,{
        course:courseId
        }, {
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            },
        })
        console.log('jjjjjj', response.data)
        if (!response.data) {
            console.log('error', response)
            alert('request failed')
        } else {
            return response.data
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }
}
export async function removeCourseFromCart (courseId:string,token:string)
{
    try {
        const response = await axios.delete(`http://0.0.0.0:8080/app/cart/remove`,{
        data : {course:courseId},
        headers: {
            'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
        }
        })
        console.log('jjjjjj', response.data)
        if (!response.data) {
            console.log('error', response)
            alert('request failed')
        } else {
            return response.data
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }
}
export async function getEnrolledCourses (token:string){
    try {
        const response = (await fetch('http://0.0.0.0:8080/app/courses/enrolled', {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            }
        }))

        if (!response.ok) {
            console.log('error', response)
            alert('request failed')
        } else {
            return await response.json()
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }  
}
export async function cartCheckout (token:string){
    try {
        const response = await axios.post(`http://0.0.0.0:8080/app/cart/checkout`,{
        }, {
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            },
        })
        if (!response.data) {
            console.log('error', response)
           
        } else {
            alert('Done!')
            return response.data
        }
    } catch (error) {
        console.log('error', error)
        alert('insufficient Fund')
    }
}
export async function isUserEnrolled (courseId:string,token:string){
    try {
        const response = await axios.get(`http://0.0.0.0:8080/app/courses/enrolled`, {
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            },
        })
        console.log('jjjjjj', response)
        if (!response.data) {
  
            console.log('error', response)
            alert('request failed')
            return false
        } else {
            const check = (response.data.map((e)=>e.id)).indexOf(courseId)
            console.log((response.data.map((e)=>e.id)).indexOf(courseId),'sssssss')
            return check !==-1
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
        return false
    }
}