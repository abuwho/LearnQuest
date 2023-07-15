import axios from 'axios'

export async function deleteCourse (courseId:string, token:string){
    try {
        const response =await  axios.delete(`http://0.0.0.0:8080/app/courses/${courseId}/delete`, {
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