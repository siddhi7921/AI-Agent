// src/components/ChatWindow.tsx

import React, { useState, useCallback, useRef } from 'react';
import { AgentMessage, AgentResponse } from '../types/AgentTypes';

// Placeholder function for calling the backend AI Agent
const callAgentApi = async (userInput: string): Promise<AgentResponse> => {
  // --- Replace this with your actual API endpoint call ---
  console.log(`Sending command to Agent: ${userInput}`);

  // Simulate API delay and different types of responses
  await new Promise(resolve => setTimeout(resolve, 1500)); 

  if (userInput.toLowerCase().includes('design')) {
    return {
      message: "I have generated a social media post for you. Click below to view the design!",
      designResultUrl: "https://via.placeholder.com/400x300.png?text=Generated+Canva+Design" // Placeholder image
    };
  } else {
    return {
      message: `Hello! You asked about: "${userInput}". I can help you design or set reminders.`,
    };
  }
};


const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSendMessage = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: AgentMessage = { id: Date.now().toString() + 'u', role: 'user', content: input.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await callAgentApi(input.trim());
      
      const agentMessage: AgentMessage = {
        id: Date.now().toString() + 'a',
        role: 'agent',
        content: response.message,
        visualOutputUrl: response.designResultUrl
      };
      
      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error("Agent API error:", error);
      const errorMessage: AgentMessage = { id: Date.now().toString() + 'e', role: 'system', content: 'Sorry, the agent encountered an error.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      scrollToBottom(); // Scroll after state update
    }
  }, [input, isLoading]);

  // useEffect to scroll to bottom after messages update
  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);


  return (
    <div className="flex flex-col h-full bg-gray-50 border border-gray-300 rounded-lg shadow-xl max-w-3xl mx-auto">
      
      {/* Messages Display Area */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div 
            key={msg.id} 
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`max-w-xs md:max-w-md p-3 rounded-lg shadow-md ${
                msg.role === 'user' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-white text-gray-800 border border-gray-200'
              }`}
            >
              <p>{msg.content}</p>
              
              {/* Render Visual Output (Canva Design Preview) */}
              {msg.visualOutputUrl && (
                <div className="mt-3 border-t pt-3 border-gray-100">
                  <p className="text-sm font-semibold mb-2">Design Preview:</p>
                  <img 
                    src={msg.visualOutputUrl} 
                    alt="Generated Design" 
                    className="w-full h-auto rounded-md"
                  />
                  <a 
                    href={msg.visualOutputUrl} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="text-sm text-blue-600 hover:underline mt-2 inline-block"
                  >
                    View Full Design
                  </a>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-700 p-3 rounded-lg shadow-md max-w-xs md:max-w-md">
              <span className="animate-pulse">Agent is thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Field */}
      <div className="p-4 border-t bg-white">
        <div className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') handleSendMessage();
            }}
            placeholder="Ask the Canva AI Agent to design something..."
            className="flex-1 p-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            className="p-3 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700 disabled:bg-blue-400 transition-colors"
            disabled={isLoading || !input.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
