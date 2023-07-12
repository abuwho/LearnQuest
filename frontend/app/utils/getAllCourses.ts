export default async function getAllCourses(token: string) {
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