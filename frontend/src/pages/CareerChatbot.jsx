import React, { useState, useRef, useEffect } from 'react';
import { 
  Bot, 
  Send, 
  User, 
  Sparkles, 
  Clock, 
  CheckCircle2, 
  HelpCircle, 
  Loader2, 
  Layers
} from 'lucide-react';
import { sendChatMessage } from '../api/client';

export default function CareerChatbot({ resumeData, matchingResult }) {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "👋 Hi! I am your **CareerFit AI Assistant**. Ask me about upcoming placement deadlines, how to prepare for interviews, why a specific company suits your profile, or how to boost your ATS score."
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestedChips, setSuggestedChips] = useState([
    "What opportunities do I have this week?",
    "What should I prepare for my interview?",
    "How do I improve my ATS score?",
    "Why is Software Engineer suitable for me?"
  ]);

  const chatBottomRef = useRef(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (messageText) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || loading) return;

    const userMessage = { sender: 'user', text: textToSend };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const skills = resumeData?.extracted_skills || [];
      const res = await sendChatMessage({
        message: textToSend,
        contextSkills: skills,
        contextCgpa: 7.8,
        contextTargetJob: matchingResult?.job_skills?.length ? 'Target Role' : 'Software Engineer'
      });

      setMessages((prev) => [...prev, { sender: 'bot', text: res.reply }]);
      if (res.suggestions && res.suggestions.length > 0) {
        setSuggestedChips(res.suggestions);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev, 
        { sender: 'bot', text: "⚠️ Sorry, I encountered an issue connecting to the CareerFit AI Core. Please check if the FastAPI backend is running." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
            Milestone 2 • Points 16 & 17
          </span>
          <span className="text-xs text-slate-400">|</span>
          <span className="text-xs text-slate-500 font-medium">Conversational Career Assistant</span>
        </div>
        <h2 className="text-xl font-bold text-slate-900 mt-1">Universal AI Career Chatbot</h2>
        <p className="text-xs text-slate-600 mt-1">
          Interactive natural language queries powered by the CareerFit Universal Chat API. Ask for deadlines, preparation plans, and profile guidance.
        </p>
      </div>

      {/* Chat Container */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col h-[600px] overflow-hidden">
        {/* Chat Messages Log */}
        <div className="flex-1 p-5 overflow-y-auto space-y-4">
          {messages.map((msg, idx) => {
            const isBot = msg.sender === 'bot';
            return (
              <div 
                key={idx} 
                className={`flex items-start space-x-3 ${isBot ? '' : 'flex-row-reverse space-x-reverse'}`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  isBot ? 'bg-indigo-600 text-white shadow-sm' : 'bg-slate-800 text-white'
                }`}>
                  {isBot ? <Bot size={16} /> : <User size={16} />}
                </div>

                <div className={`max-w-[80%] rounded-2xl p-4 text-xs leading-relaxed ${
                  isBot 
                    ? 'bg-slate-50 border border-slate-200 text-slate-800 whitespace-pre-line' 
                    : 'bg-indigo-600 text-white shadow-sm'
                }`}>
                  {msg.text}
                </div>
              </div>
            );
          })}

          {loading && (
            <div className="flex items-center space-x-3 text-slate-400 text-xs py-2">
              <div className="w-8 h-8 rounded-full bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-600">
                <Loader2 size={16} className="animate-spin" />
              </div>
              <span>CareerFit AI Assistant is formulating response...</span>
            </div>
          )}

          <div ref={chatBottomRef} />
        </div>

        {/* Suggestion Chips */}
        {suggestedChips.length > 0 && (
          <div className="px-5 py-2.5 bg-slate-50 border-t border-slate-100 flex flex-wrap gap-1.5 items-center">
            <span className="text-[10px] font-bold uppercase text-slate-400 mr-1 flex items-center space-x-1">
              <Sparkles size={11} className="text-amber-500" />
              <span>Suggested:</span>
            </span>
            {suggestedChips.map((chip, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(chip)}
                className="text-[11px] bg-white border border-slate-200 hover:border-indigo-400 text-slate-700 px-2.5 py-1 rounded-full font-medium transition-all hover:bg-indigo-50/50"
              >
                {chip}
              </button>
            ))}
          </div>
        )}

        {/* Chat Input Bar */}
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="p-4 bg-white border-t border-slate-200 flex items-center space-x-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your placement question or prep query..."
            className="flex-1 text-xs border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl text-xs font-semibold shadow-sm flex items-center space-x-1.5 transition-colors"
          >
            <span>Send</span>
            <Send size={14} />
          </button>
        </form>
      </div>

      {/* Architectural Note (Point 17) */}
      <div className="bg-slate-900 text-slate-300 rounded-xl p-4 text-xs space-y-2 border border-slate-800">
        <div className="flex items-center space-x-2 text-indigo-400 font-bold">
          <Layers size={14} />
          <span>Point 17 — Platform-Independent Architecture Disclosure</span>
        </div>
        <p className="text-[11px] text-slate-400 leading-relaxed">
          The CareerFit chatbot engine is decoupled from frontend channels. The underlying <code>/api/chat/message</code> Universal Chat API can be linked via webhook adapters to Telegram, WhatsApp, or Discord bots without modifying core AI reasoning logic.
        </p>
      </div>
    </div>
  );
}
