import { useToast } from '@apideck/components'
import { ChatCompletionRequestMessage } from 'openai'
import {
  ReactNode,
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react'

interface ContextProps {
  messages: ChatCompletionRequestMessage[]
  addMessage: (content: string) => Promise<void>
  isLoadingAnswer: boolean
}

const ChatsContext = createContext<Partial<ContextProps>>({})

const apiKey = process.env.OPENAI_API_KEY
// console.log(apiKey)
const url = 'https://api.openai.com/v1/chat/completions'

export function MessagesProvider({ children }: { children: ReactNode }) {
  const { addToast } = useToast()
  const [messages, setMessages] = useState<ChatCompletionRequestMessage[]>([])
  const [isLoadingAnswer, setIsLoadingAnswer] = useState(false)

  useEffect(() => {
    const initializeChat = () => {
      // const welcomeMessage: ChatCompletionRequestMessage = {
      //   role: 'assistant',
      //   content: 'Hi, How can I help you today?',
      // }
      // setMessages([systemMessage])
    }

    // When no messages are present, we initialize the chat the system message and the welcome message
    // We hide the system message from the user in the UI
    if (!messages?.length) {
      // initializeChat()
    }
  }, [messages?.length, setMessages]);

  const addMessage = async (content: string) => {
    setIsLoadingAnswer(true)
    try {
      const newMessage: ChatCompletionRequestMessage = {
        role: 'user',
        content: content,
      }
      const newMessages = [...messages, newMessage]

      // Add the user message to the state so we can see it immediately
      setMessages(newMessages)

      const body = JSON.stringify({
        messages: [
          { role: 'system', content: 'You are ChatGPT, a large language model trained by OpenAI.'},
          { role: 'user', content: content }
        ],
        model: 'gpt-3.5-turbo',
        stream: false,
      })

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
        },
        body,
      })
      const data = await response.json()
    
      console.log(data)
      const reply = data.choices[0].message
      console.log(reply)

      // Add the assistant message to the state
      setMessages([...newMessages, reply])
    } catch (error) {
      // Show error when something goes wrong
      console.log(error);
    } finally {
      setIsLoadingAnswer(false)
    }
  };

  return (
    <ChatsContext.Provider value={{ messages, addMessage, isLoadingAnswer }}>
        {children}
    </ChatsContext.Provider>
  )
}

export const useMessages = () => {
  return useContext(ChatsContext) as ContextProps
}
