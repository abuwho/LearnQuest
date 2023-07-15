import axios from 'axios'
import { getBaseURL } from './getBaseURL'

export async function getAllCreatedCourses(token: string) {
    const url = `${getBaseURL()}/app/courses/created`
    try {
        const response = (await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            }
        }))

        if (!response.ok) {
            console.log('error', response)
            return []
            alert('request failed')
        } else {
            return await response.json()
        }
    } catch (error) {
        console.log('error', error)
        return []
        alert('request failed')
    }
}
export async function getAuthorizedViewCourse(courseId: string, token: string) {
    const url = `${getBaseURL()}/app/courses/${courseId}/preview`
    try {
        const response = await axios.get(url, {
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
    const url = `${getBaseURL()}/app/cart/get`
    try {
        const response = await axios.get(url, {
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
    const url = `${getBaseURL()}/app/cart/add`
    try {
        const response = await axios.post(url, {
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
export async function removeCourseFromCart (courseId:string,token:string) {
    const url = `${getBaseURL()}/app/cart/remove`
    try {
        const response = await axios.delete(url, {
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
    const url = `${getBaseURL()}/app/courses/enrolled`
    try {
        const response = (await fetch(url, {
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
    const url = `${getBaseURL()}/app/cart/checkout`
    try {
        const response = await axios.post(url, {
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
    const url = `${getBaseURL()}/app/courses/enrolled`
    try {
        const response = await axios.get(url, {
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