import axios from 'axios'
export async function getAllCreatedCourses(token: string) {
    try {
        const response =  (await fetch('http://0.0.0.0:8080/app/courses/created', {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            }
        }))

        if (!response.ok) {
            console.log('error', response)
            alert('request failed')
        } else {
            return  await response.json()
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }
}
export async function getAuthorizedViewCourse (courseId:string, token:string){
    try {
        const response =await  axios.get(`http://0.0.0.0:8080/app/courses/${courseId}/full_view`, {
            headers: {
                'Authorization': `Token ${token}`,  // Assuming `token` is in the scope
            },
        })
        console.log('jjjjjj',response)
        if (!response.data) {
            console.log('error', response)
            alert('request failed')
        } else {
            return  response.data
        }
    } catch (error) {
        console.log('error', error)
        alert('request failed')
    }
}