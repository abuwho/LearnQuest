import { ChatCompletionRequestMessage } from 'openai'

export const sendMessage = async (messages: ChatCompletionRequestMessage[]) => {
  const apiKey = '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'
  const url = 'https://api.openai.com/v1/chat/completions'

  const body = JSON.stringify({
    messages,
    model: 'gpt-3.5-turbo',
    stream: false,
  })

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body,
    })
    const data = await response.json()
    return data;
  } catch (error) {
    response.status(500).json({ error: error.message })
  }
};
