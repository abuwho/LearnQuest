"use client"
import './globals.css';
import Navbar from './components/Navbar/index';
import Footer from './components/Footer/Footer';
import { useState, createContext, useEffect } from 'react';
import axios from 'axios'
import { connect } from 'http2';

export const UserContext = createContext<{
  userId: string,
  token: string,
  setToken: (token: string) => void,
  isLoggingIn: boolean,
  setIsLoggingIn: (isLoggingIn: boolean) => void
} | null>(null)

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [userId, setUserId] = useState<string>('')
  const [token, setToken] = useState<string>('')
  const [isLoggingIn, setIsLoggingIn] = useState<boolean>(false)
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false)
  const userContextValue = {
    userId: userId,
    token: token,
    setToken: (newToken: string) => {
      localStorage.setItem('token', newToken)
      setToken(newToken)
    },

   
    isLoggingIn: isLoggingIn,
    setIsLoggingIn: setIsLoggingIn
  }
  useEffect(() => {
    console.log('token', token)
  }, [token])
  useEffect(() => {
    console.log('ssssss', userId)
  }, [])

  const connectAccount = async () => {
    console.log(token, 'llllll')
    if (!token || token === '') {
      setIsLoggedIn(false)
      setUserId('')
      return
    }
    console.log(token, 'oooooo')

    try {
      const response = await axios.get('http://0.0.0.0:8080/auth/get_current_user/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      console.log('userId', response.data.id)
      setUserId(response.data.id)
    } catch (e) {
      console.log(e)
      setIsLoggedIn(false)
      setUserId('')
      return
    }
  }
      useEffect(()=>{
        const storedToken = localStorage.getItem('token')
        if(!storedToken) return
        setToken(storedToken)
    },[])
  useEffect(() => {
    connectAccount()
  }, [token])

  return (
    <html lang="en">
      <body>

        <UserContext.Provider value={userContextValue}>
          <Navbar />
          {children}
          <Footer />
        </UserContext.Provider>
      </body>
    </html>
  )
}
