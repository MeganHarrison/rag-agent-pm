'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ragClient, type ChatMessage } from '@/lib/rag-client';

export default function ChatComponent() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [streamingMessage, setStreamingMessage] = useState('');
  const [apiUrl, setApiUrl] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Generate session ID and get API URL on mount
    setSessionId(crypto.randomUUID());
    setApiUrl(ragClient.getApiUrl());
    
    // Test connection on mount
    ragClient.health().then(
      (health) => console.log('RAG API healthy:', health),
      (error) => console.error('RAG API health check failed:', error)
    );
  }, []);

  useEffect(() => {
    // Auto-scroll to bottom
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMessage]);

  const sendStreamingMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setIsLoading(true);
    setStreamingMessage('');
    
    // Add user message
    const newMessages = [...messages, { role: 'user' as const, content: userMessage }];
    setMessages(newMessages);

    try {
      let accumulatedMessage = '';
      let toolCalls: Array<{ tool: string; args: any }> = [];

      for await (const event of ragClient.chatStream({
        message: userMessage,
        conversation_history: newMessages,
        session_id: sessionId,
      })) {
        if (event.type === 'text') {
          accumulatedMessage += event.data;
          setStreamingMessage(accumulatedMessage);
        } else if (event.type === 'tool_call') {
          toolCalls.push(event.data);
        } else if (event.type === 'complete') {
          setMessages([
            ...newMessages,
            {
              role: 'assistant',
              content: event.data.response,
            },
          ]);
          setStreamingMessage('');
        } else if (event.type === 'error') {
          throw new Error(event.data);
        }
      }
    } catch (error) {
      console.error('Stream error:', error);
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error processing your request.',
        },
      ]);
      setStreamingMessage('');
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setIsLoading(true);
    
    // Add user message
    const newMessages = [...messages, { role: 'user' as const, content: userMessage }];
    setMessages(newMessages);

    try {
      const data = await ragClient.chat({
        message: userMessage,
        conversation_history: newMessages,
        session_id: sessionId,
      });
      
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: data.response,
        },
      ]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error processing your request.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="mb-4 p-4 bg-blue-600 text-white rounded-lg">
        <h1 className="text-2xl font-bold">RAG Agent Chat</h1>
        <div className="text-sm opacity-90">
          <p>Session: {sessionId.slice(0, 8)}...</p>
          <p className="text-xs">API: {apiUrl}</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-50 rounded-lg p-4 mb-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p>Start a conversation by typing a message below.</p>
            <p className="text-sm mt-2">I can search the knowledge base to answer your questions.</p>
          </div>
        )}
        
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-4 ${
              message.role === 'user' ? 'text-right' : 'text-left'
            }`}
          >
            <div
              className={`inline-block p-3 rounded-lg max-w-[80%] ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white border border-gray-200'
              }`}
            >
              <div className="text-sm font-semibold mb-1">
                {message.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div className="whitespace-pre-wrap">{message.content}</div>
            </div>
          </div>
        ))}
        
        {/* Streaming message */}
        {streamingMessage && (
          <div className="mb-4 text-left">
            <div className="inline-block p-3 rounded-lg max-w-[80%] bg-white border border-gray-200">
              <div className="text-sm font-semibold mb-1">Assistant</div>
              <div className="whitespace-pre-wrap">{streamingMessage}</div>
            </div>
          </div>
        )}
        
        {/* Loading indicator */}
        {isLoading && !streamingMessage && (
          <div className="text-center text-gray-500">
            <div className="inline-flex items-center">
              <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Searching knowledge base...
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              sendStreamingMessage();
            }
          }}
          placeholder="Ask a question..."
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
          className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
        <button
          onClick={sendStreamingMessage}
          disabled={isLoading || !input.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Stream
        </button>
      </div>
    </div>
  );
}