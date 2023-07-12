"use client"
import './globals.css';
import Navbar from './components/Navbar/index';
import Footer from './components/Footer/Footer';
import { useState, createContext, useEffect } from 'react';
import axios from 'axios'
import { connect } from 'http2';
import SignIn from '/Users/alimansour/testdir/LearnQuest/frontend/app/components/Navbar/Signdialog.tsx'
import { convertToObject } from 'typescript';
type userIdType = {
  id: string,
  username: string,
  email: string

}
const emtpyUserId = {
  id: '',
  username: '',
  email: ''
}
export const UserContext = createContext<{
  userId: userIdType | undefined,
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
  const [userId, setUserId] = useState<userIdType>()
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


  const connectAccount = async () => {
    if (!token || token === '') {
      setIsLoggedIn(false)
      setUserId({
        id: '',
        username: '',
        email: ''
      })
      return
    }
    try {
      const response = await axios.get('http://0.0.0.0:8080/auth/get_current_user/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      const user = response.data.user
      setUserId({ username: user.username, email: user.email, id: user.id })
    } catch (e) {
      console.log(e,'userid')
      setIsLoggedIn(false)
      setUserId(emtpyUserId)
      return
    }

  }

  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (!storedToken) return
    setToken(storedToken)
  }, [])
  useEffect(() => {
    connectAccount()
  }, [token])
  useEffect(() => {
    console.log('userId', userId)
  }, [userId])
  return (
    <html lang="en">

      <UserContext.Provider value={userContextValue}>
        <body>

          <Navbar />
          {children}
          <Footer />
        </body>

      </UserContext.Provider>
    </html>
  )
}
