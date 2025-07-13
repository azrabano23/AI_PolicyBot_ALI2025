import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, ExternalLink, Calendar, Users, FileText, Home, ChevronLeft, ChevronRight, Star, Flag, Heart } from 'lucide-react';

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
      const apiUrl = process.env.NODE_ENV === 'production' ? '/api/chat' : 'http://localhost:8085/api/chat';
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

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  
  // Auto-advance carousel every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentQuestionIndex((prev) => (prev + 1) % 18); // 18 is the total number of questions
    }, 5000);
    return () => clearInterval(interval);
  }, []);
  
  const quickQuestions = [
    { icon: User, text: "Mussab doesn't have any experience – why should I vote for him?", category: "experience", color: "bg-red-500" },
    { icon: FileText, text: "Mussab just has talking points but no concrete policy proposals.", category: "policy", color: "bg-blue-500" },
    { icon: Calendar, text: "When he was president the school board budget increased which led to higher taxes, I don't like that!", category: "taxes", color: "bg-green-500" },
    { icon: Users, text: "There is a lot of corruption on the school board, a group that Mussab is strongly affiliated with. I don't want more corruption in Jersey City.", category: "corruption", color: "bg-purple-500" },
    { icon: Star, text: "I haven't heard of him before – is Mussab a serious candidate?", category: "candidate", color: "bg-yellow-500" },
    { icon: Heart, text: "Why is Mussab's faith so important to him? Why does he need to mention it as a part of his story?", category: "faith", color: "bg-pink-500" },
    { icon: Users, text: "Jersey City has gotten more dangerous over the years. What's Mussab going to do about that?", category: "safety", color: "bg-red-600" },
    { icon: Home, text: "Public transit is more expensive and worse quality than ever in Jersey City!", category: "transit", color: "bg-blue-600" },
    { icon: Home, text: "I can't afford to buy a house in Jersey City anymore and rent is too expensive.", category: "housing", color: "bg-green-600" },
    { icon: FileText, text: "It's hard to find a good job with a fair wage to afford to live in Jersey City anymore. How is Mussab going to improve that?", category: "jobs", color: "bg-purple-600" },
    { icon: Users, text: "I pay a lot to live in Jersey City and the public schools for my kids aren't very good. How is Mussab going to improve them?", category: "schools", color: "bg-indigo-500" },
    { icon: Flag, text: "What is Mussab going to do to combat climate change as Mayor of Jersey City?", category: "climate", color: "bg-emerald-500" },
    { icon: Users, text: "I'm sick of all the corruption in our city! How is Mussab going to change that?", category: "corruption_general", color: "bg-red-700" },
    { icon: Star, text: "I really liked our previous Mayor Fulop. Why should I vote for Mussab – isn't he anti-Fulop?", category: "fulop_positive", color: "bg-blue-700" },
    { icon: User, text: "I disliked our previous Mayor Fulop. How is Mussab going to be different?", category: "fulop_negative", color: "bg-slate-600" },
    { icon: Users, text: "I want to vote for Jim McGreevey, why should I vote for Mussab?", category: "mcgreevey", color: "bg-gray-600" },
    { icon: Users, text: "I want to vote for Bill O'Dea, why should I vote for Mussab?", category: "odea", color: "bg-orange-600" },
    { icon: Users, text: "I want to vote for James Solomon, why should I vote for Mussab?", category: "solomon", color: "bg-teal-600" }
  ];
  
  const nextQuestion = () => {
    setCurrentQuestionIndex((prev) => (prev + 1) % quickQuestions.length);
  };
  
  const prevQuestion = () => {
    setCurrentQuestionIndex((prev) => (prev - 1 + quickQuestions.length) % quickQuestions.length);
  };

  const handleQuickQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-blue-50">
      {/* Header */}
    <div className="bg-gradient-to-r from-red-600 to-blue-600 shadow-sm border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-red-600 to-blue-600 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Ali 2025 Campaign Assistant</h1>
              <p className="text-sm text-red-100">Real-time Policy & Campaign Information</p>
            </div>
            <div className="ml-auto">
              <a 
                href="https://www.ali2025.com/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-white hover:text-red-100 transition-colors duration-200"
              >
                <ExternalLink className="w-4 h-4" />
                <span className="font-medium">Visit ali2025.com</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Questions Carousel */}
      <div className="max-w-5xl mx-auto px-6 py-6">
        <div className="bg-gradient-to-r from-red-100 to-blue-100 p-6 rounded-xl shadow-sm border border-slate-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-slate-800 flex items-center space-x-2">
              <Flag className="w-5 h-5 text-red-600" />
              <span>Common Questions About Mussab Ali</span>
            </h2>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-slate-600 font-medium">
                {currentQuestionIndex + 1} of {quickQuestions.length}
              </span>
              <button
                onClick={prevQuestion}
                className="p-2 rounded-full bg-white shadow-sm border border-slate-200 hover:border-blue-300 hover:shadow-md transition-all duration-200"
              >
                <ChevronLeft className="w-4 h-4 text-slate-600" />
              </button>
              <button
                onClick={nextQuestion}
                className="p-2 rounded-full bg-white shadow-sm border border-slate-200 hover:border-blue-300 hover:shadow-md transition-all duration-200"
              >
                <ChevronRight className="w-4 h-4 text-slate-600" />
              </button>
            </div>
          </div>
          
          <div className="relative overflow-hidden">
            <div className="flex transition-transform duration-300 ease-in-out" style={{ transform: `translateX(-${currentQuestionIndex * 100}%)` }}>
              {quickQuestions.map((question, index) => {
                const IconComponent = question.icon;
                return (
                  <div key={index} className="w-full flex-shrink-0">
                    <button
                      onClick={() => handleQuickQuestion(question.text)}
                      className="w-full p-6 bg-white rounded-lg shadow-sm border border-slate-200 hover:border-blue-300 hover:shadow-md transition-all duration-200 text-left group"
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`w-12 h-12 ${question.color} rounded-full flex items-center justify-center flex-shrink-0 shadow-sm`}>
                          <IconComponent className="w-6 h-6 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-slate-500 uppercase tracking-wide mb-1">{question.category}</div>
                          <p className="text-base font-semibold text-slate-800 group-hover:text-slate-900 leading-relaxed">
                            {question.text}
                          </p>
                          <div className="mt-3 text-xs text-blue-600 font-medium group-hover:text-blue-700 transition-colors duration-200">
                            Click to ask this question →
                          </div>
                        </div>
                      </div>
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
          
          {/* Question indicators */}
          <div className="flex justify-center mt-4 space-x-2">
            {quickQuestions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestionIndex(index)}
                className={`w-2 h-2 rounded-full transition-all duration-200 ${
                  index === currentQuestionIndex ? 'bg-blue-600' : 'bg-slate-300 hover:bg-slate-400'
                }`}
              />
            ))}
          </div>
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
