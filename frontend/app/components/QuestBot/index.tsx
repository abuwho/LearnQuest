"use client"

import MessageForm from './MessageForm'
import MessagesList from './MessagesList'
import { NextPage } from 'next'
import { MessagesProvider } from './useMessages'

export default function QuestBot() {

  return (
    <MessagesProvider>
      <MessagesList />
        <MessageForm />
    </MessagesProvider>
  )
}