"use client"
import Banner from './components/Banner/index';
import Companies from './components/Companies/Companies';
import Courses from './components/Courses/index';
import Mentor from './components/Mentor/index';
import Testimonials from './components/Testimonials/index';
import Newsletter from './components/Newsletter/Newsletter';
import { createContext, useState } from 'react'
import axios from 'axios'


export default function Home() {

 

  return (
    
    <main>
        <Banner />
        <Companies />
        <Courses />
        <Mentor />
        <Testimonials />
        <Newsletter />
    </main>
    
  )
}
