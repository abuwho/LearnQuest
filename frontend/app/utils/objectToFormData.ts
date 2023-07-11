export default function objectToFormData(obj: Record<string, any>): FormData {
    const formData = new FormData();

    for (let key in obj) {
        formData.append(key, obj[key]);
    }

    return formData;
}