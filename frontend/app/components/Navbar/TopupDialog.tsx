"use client"

import { Dialog, Transition } from '@headlessui/react'
import { Fragment, SetStateAction, useContext, useEffect, useState } from 'react'
import { CreditCardIcon} from '@heroicons/react/20/solid'
import { UserContext } from '@/app/layout.tsx'
import { getBaseURL } from '@/app/utils/getBaseURL'
import { border } from '@chakra-ui/react'


const TopupDialog = () => {
    let [isOpen, setIsOpen] = useState(false)

    const {isLoggingIn,setIsLoggingIn, setToken,token,userId}= useContext(UserContext)!

    const [cardHolder, setCardHolder] = useState('');
    const [cardNumber, setCardNumber] = useState('');
    const [expiryDate, setExpiryDate] = useState('');
    const [cvv, setCvv] = useState('');
    const [amount, setAmount] = useState('');

    const [currentBalance, setCurrentBalance] = useState('...loading');
    const [userName, setUserName] = useState('...loading');

    useEffect(() => {
        getCurrentUser().then((data) => {
            setCurrentBalance(data.wallet.balance);
        });
    });

    useEffect(() => {
        getCurrentUser().then((data) => {
            setUserName(data.user.username);
        });
    });

    const closeModal = () => {
        setIsOpen(false)
    }

    const openModal = () => {
        setIsOpen(true)
    }

    const getCurrentUser = async () => {
        try {
            const token = localStorage.getItem('token')

            const url = getBaseURL() + '/auth/get_current_user/';

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    Authorization: `Token ${token}`,
                    'Content-Type': 'application/json'
                },
            });

            console.log(response);

            if (response.ok) {
                console.log('Current user fetched successfully');
                const data = await response.json()
                console.log(data);
                return data;
            } else {
                console.error('Failed to fetch current user while getting balance');
            }
        } catch (error) {
            console.error('Error occurred while getting balance:', error);
        }
    }

    const topupHandler = async (event: { preventDefault: () => void }) => {
        event.preventDefault(); // Prevent the form from submitting and refreshing the page
        
        try {
            const token = localStorage.getItem('token')
            const requestBody = {
                amount: amount,
            };

            const url = getBaseURL() + '/auth/topup/'
            const response = await fetch(url, {
            method: 'POST',
            headers: {
                Authorization: `Token ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
            });

            console.log(response);

            // Check if the registration was successful
            if (response.ok) {
                console.log('Topup successful');
                const data = await response.json()
                console.log(data);
            } else {
                console.error('Topup failed');
            }
        } catch (error) {
            console.error('Error occurred during top up:', error);
        }
      };
      

    return (
        <>
            <div className="absolute inset-y-0 right-0 flex items-center sm:static sm:inset-auto sm:pr-0">
                <div className='hidden lg:block'>
                    <button type="button" className='text-lg text-Blueviolet font-medium' onClick={openModal}>
                        Topup
                    </button>
                </div>
            </div>

            <Transition appear show={isOpen} as={Fragment}>
                <Dialog as="div" className="relative z-10" onClose={closeModal}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </Transition.Child>

                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4 text-center">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">

                                    <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                                        <div className="w-full max-w-md space-y-8">
                                            <div>
                                                <img
                                                    className="mx-auto h-12 w-auto"
                                                    src="/assets/logo/logo.svg"
                                                    alt="LearnQuest"
                                                />
                                                <p className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                                                    Hi, { userName }!
                                                </p>
                                                <p className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                                                    Current balance: ${ currentBalance }
                                                </p>
                                                <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                                                    Topup your account
                                                </h2>
                                            </div>
                                            <form className="mt-8 space-y-6" action="/auth/login" method="POST" onSubmit={topupHandler}>
                                                <input type="hidden" name="remember" defaultValue="true" />
                                                <div className="-space-y-px rounded-md shadow-sm">
                                                    <div>
                                                        <label htmlFor='cardHolder' className='sr-only'>
                                                            Card holder
                                                        </label>
                                                        <input
                                                            type="text"
                                                            name="cardHolder"
                                                            id="cardHolder"
                                                            value={cardHolder}
                                                            onChange={(e) => setCardHolder(e.target.value)}
                                                            className="relative block w-full appearance-none rounded-none rounded-t-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="John Smith"
                                                        />
                                                    </div>
                                                    <div>
                                                        <label htmlFor="cardNumber" className="sr-only">
                                                            Card number
                                                        </label>
                                                        <input 
                                                            type="text"
                                                            name="cardNumber"
                                                            id="cardNumber"
                                                            value={cardNumber}
                                                            onChange={(e) => setCardNumber(e.target.value)}
                                                            className="relative block w-full appearance-none rounded-none rounded-t-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="4242 4242 4242 4242"
                                                        />
                                                    </div>

                                                    <div>
                                                        <label htmlFor='expiryDate' className='sr-only'>
                                                            Expiry date
                                                        </label>
                                                        <input
                                                            type="text"
                                                            name="expiryDate"
                                                            id="expiryDate"
                                                            value={expiryDate}
                                                            className="relative block w-full appearance-none rounded-none rounded-t-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="MM/YY"
                                                            onChange={(e) => setExpiryDate(e.target.value)}
                                                        />
                                                    </div>

                                                    <div>
                                                        <label htmlFor='cvv' className='sr-only'>
                                                            CVV
                                                        </label>
                                                        <input
                                                            type="number"
                                                            name="cvv"
                                                            id="cvv"
                                                            value={cvv}
                                                            className="relative block w-full appearance-none rounded-none rounded-t-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="CVV"
                                                            onChange={(e) => setCvv(e.target.value)}
                                                        />
                                                    </div>

                                                    <div>
                                                        <label htmlFor='amount' className='sr-only'>
                                                            Amount
                                                        </label>
                                                        <input
                                                            type="number"
                                                            name="amount"
                                                            id="cvv"
                                                            value={amount}
                                                            className="relative block w-full appearance-none rounded-none rounded-t-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="in USD"
                                                            onChange={(e) => setAmount(e.target.value)}
                                                        />
                                                    </div>

                                                </div>

                                                <div>
                                                    <button
                                                        type="submit"
                                                        className="group relative flex w-full justify-center rounded-md border border-transparent bg-Blueviolet py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                                    >
                                                        <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                                                            <CreditCardIcon className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
                                                        </span>
                                                        Topup
                                                    </button>
                                                </div>
                                            </form>
                                        </div>
                                    </div>


                                    <div className="mt-4 flex justify-end">
                                        <button
                                            type="button"
                                            className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                                            onClick={closeModal}
                                        >
                                            ❌ Close
                                        </button>
                                    </div>
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>
        </>
    )
}

export default TopupDialog;
