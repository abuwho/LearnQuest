"use client"

import MessageForm from '@/app/components/MessageForm'
import MessagesList from '@/app/components/MessagesList'
import { NextPage } from 'next'
import { MessagesProvider } from '@/app/components/useMessages'

export default function QuestBot() {

  return (
    <MessagesProvider>
      <MessagesList />
        <MessageForm />
    </MessagesProvider>
  )
}