import axios from 'axios'
import { getBaseURL } from './getBaseURL'

export async function deleteCourse (courseId:string, token:string){
    const url = `${getBaseURL()}/app/courses/${courseId}/delete`
    try {
        const response =await  axios.delete(url, {
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