"use client"
import Slider from "react-slick";
import React, { Component } from "react";
import { StarIcon } from '@heroicons/react/24/solid';
import Image from "next/image";

// CAROUSEL DATA

interface DataType {
    profession: string;
    comment: string;
    imgSrc: string;
    name: string;
}

const postData: DataType[] = [
    {
        name: "Emma",
        profession: 'LearnQuest student',
        comment: "Thanks to LearnQuest, I have successfully transitioned into a new career and achieved professional growth.",
        imgSrc: '/assets/testimonial/user.svg',
    },
    {
        name: "Leslie",
        profession: 'LearnQuest instructor',
        comment: 'As an instructor, LearnQuest has provided me with a remarkable platform to share my knowledge and expertise with a global audience.',
        imgSrc: '/assets/mentor/user2.png',
    },
    {
        name: "Cody",
        profession: 'CEO, Parkview Int.Ltd',
        comment: ' LearnQuest has become my go-to destination for continuous learning, and I highly recommend it to anyone looking to broaden their knowledge and grow both personally and professionally.',
        imgSrc: '/assets/mentor/user3.png',
    },
    {
        name: "Robert",
        profession: 'Product Manager, Meta',
        comment: 'LearnQuest has completely transformed the way I learn with the platform\'s diverse range of courses,',
        imgSrc: '/assets/mentor/user1.png',
    },
    {
        name: "Pamela",
        profession: 'Analyst, Instructor',
        comment: 'Joining LearnQuest has expanded my reach as an instructor and enabled me to make a significant impact in the lives of learners.',
        imgSrc: '/assets/mentor/user2.png',
    },
    {
        name: "Walter",
        profession: 'Analyst',
        comment: 'The personalized learning paths and interactive features make the learning experience engaging and enjoyable.',
        imgSrc: '/assets/mentor/user3.png',
    },
]

// CAROUSEL SETTINGS


export default class MultipleItems extends Component {

    render() {
        const settings = {
            dots: true,
            dotsClass: "slick-dots",
            infinite: true,
            slidesToShow: 3,
            // centerMode: true,
            slidesToScroll: 2,
            arrows: false,
            autoplay: false,
            speed: 500,
            autoplaySpeed: 2000,
            cssEase: "linear",
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1,
                        infinite: true,
                        dots: false
                    }
                },
                {
                    breakpoint: 800,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1,
                        infinite: true,
                        dots: false
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        infinite: true,
                        dots: false
                    }
                }
            ]
        };

        return (
            <div className="pt-40 pb-10 sm:pb-32 lg:py-32" id="testimonial">
                <div className='mx-auto max-w-7xl sm:py-4 lg:px-8'>
                    <Slider {...settings}>
                        {postData.map((items, i) => (
                            <div key={i}>
                                <div className={`bg-white m-4 p-5 my-20 relative ${i % 2 ? 'middleDiv' : 'testimonial-shadow'}`}>
                                    <div className="absolute top-[-45px]">
                                        <Image src={items.imgSrc} alt={items.imgSrc} width={100} height={100} className="inline-block" />
                                    </div>
                                    <h4 className='text-base font-normal text-darkgray my-4'>{items.comment}</h4>
                                    <hr style={{ color: "#D7D5D5" }} />
                                    <div className="flex justify-between">
                                        <div>
                                            <h3 className='text-lg font-medium text-darkbrown pt-4 pb-2'>{items.name}</h3>
                                            <h3 className='text-sm font-normal text-lightgray pb-2'>{items.profession}</h3>
                                        </div>
                                        <div className="flex">
                                            <StarIcon width={20} className="text-gold" />
                                            <StarIcon width={20} className="text-gold" />
                                            <StarIcon width={20} className="text-gold" />
                                            <StarIcon width={20} className="text-gold" />
                                            <StarIcon width={20} className="text-lightgray" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </Slider>
                </div>
            </div>

        );
    }
}
