export const getBaseURL = () => {
    if (process.env.NEXT_PUBLIC_API_BASE_URL) {
      return process.env.NEXT_PUBLIC_API_BASE_URL;
    } 
    // Fallback URL if environment variable is not defined
    return 'http://localhost:8000';
};