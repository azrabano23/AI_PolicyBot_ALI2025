import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, ExternalLink, Calendar, Users, FileText, Home } from 'lucide-react';

const Ali2025AdvancedBot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hi! I'm Ali 2025's Campaign Assistant. I'm here to help you learn about Mussab Ali's policies, campaign events, and how to get involved in the 2025 Jersey City mayoral race. What would you like to know?",
      timestamp: new Date(),
      sources: []
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isSearching) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsSearching(true);

    try {
      // Call your backend API here
      const apiUrl = process.env.NODE_ENV === 'production' ? 'http://localhost:8081/api/chat' : '/api/chat';
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: 'default'
        }),
      });

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.response || "I'm processing your question about Mussab Ali's campaign. Please try again in a moment.",
        timestamp: new Date(),
        sources: data.sources || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I'm having trouble accessing the latest campaign information right now. Please try again in a moment.",
        timestamp: new Date(),
        sources: []
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    { icon: Home, text: "What are Mussab's housing policies?", category: "policy" },
    { icon: Users, text: "How can I volunteer for the campaign?", category: "volunteer" },
    { icon: Calendar, text: "What are upcoming campaign events?", category: "events" },
    { icon: FileText, text: "What's Mussab's stance on education?", category: "policy" }
  ];

  const handleQuickQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-red-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-red-600 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-800">Ali 2025 Campaign Assistant</h1>
              <p className="text-sm text-slate-500">Real-time Policy & Campaign Information</p>
            </div>
            <div className="ml-auto">
              <a 
                href="https://www.ali2025.com/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 transition-colors duration-200"
              >
                <ExternalLink className="w-4 h-4" />
                <span className="font-medium">Visit ali2025.com</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Questions */}
      <div className="max-w-5xl mx-auto px-6 py-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {quickQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => handleQuickQuestion(question.text)}
              className="p-3 bg-white rounded-lg shadow-sm border border-slate-200 hover:border-blue-300 hover:shadow-md transition-all duration-200 text-left group"
            >
              <div className="flex items-center space-x-3">
                <question.icon className="w-4 h-4 text-slate-400 group-hover:text-blue-500 transition-colors duration-200" />
                <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900">{question.text}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Messages Container */}
      <div className="max-w-5xl mx-auto px-6 pb-32">
        <div className="space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex space-x-3 max-w-4xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                <div className="flex-shrink-0">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    message.type === 'user' 
                      ? 'bg-slate-200' 
                      : 'bg-gradient-to-r from-blue-600 to-red-600'
                  }`}>
                    {message.type === 'user' ? (
                      <User className="w-4 h-4 text-slate-600" />
                    ) : (
                      <Bot className="w-4 h-4 text-white" />
                    )}
                  </div>
                </div>
                <div className={`flex-1 ${message.type === 'user' ? 'text-right' : ''}`}>
                  <div className={`inline-block p-4 rounded-2xl shadow-sm ${
                    message.type === 'user'
                      ? 'bg-slate-100 text-slate-800 rounded-br-md'
                      : 'bg-white border border-slate-200 rounded-bl-md'
                  }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-slate-200">
                        <p className="text-xs font-medium text-slate-500 mb-2">Sources:</p>
                        <div className="space-y-1">
                          {message.sources.map((source, index) => (
                            <a
                              key={index}
                              href={source.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center space-x-2 text-xs text-blue-600 hover:text-blue-700 transition-colors duration-200"
                            >
                              <ExternalLink className="w-3 h-3" />
                              <span>{source.title}</span>
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-2 px-1">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            </div>
          ))}
          {isSearching && (
            <div className="flex justify-start">
              <div className="flex space-x-3 max-w-4xl">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 rounded-full flex items-center justify-center bg-gradient-to-r from-blue-600 to-red-600">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                </div>
                <div className="flex-1">
                  <div className="inline-block p-4 rounded-2xl rounded-bl-md bg-white border border-slate-200 shadow-sm">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 shadow-2xl">
        <div className="max-w-5xl mx-auto w-full">
          <div className="p-6">
            <div className="flex space-x-4">
              <div className="flex-1 relative">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about policies, latest updates, campaign events, or how to get involved..."
                  className="w-full p-4 border-2 border-slate-200 rounded-xl resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 text-slate-700 placeholder-slate-400 shadow-sm"
                  rows="2"
                />
              </div>
              <button
                onClick={handleSend}
                disabled={!inputValue.trim() || isSearching}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-red-600 text-white rounded-xl hover:from-blue-700 hover:to-red-700 disabled:from-slate-300 disabled:to-slate-300 disabled:cursor-not-allowed transition-all duration-200 flex items-center shadow-lg hover:shadow-xl font-semibold"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <div className="mt-4 text-xs text-slate-400 text-center font-medium">
              Ali 2025 Campaign • Real-time Campaign Intelligence • ali2025.com
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Ali2025AdvancedBot;
