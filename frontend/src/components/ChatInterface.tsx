"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Paperclip, Trash2, Loader, FileText, Square } from "lucide-react";
import { toast } from "sonner";

// Format timestamp to avoid hydration issues
const formatTime = (dateOrString: Date | string): string => {
  const date = typeof dateOrString === "string" ? new Date(dateOrString) : dateOrString;
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${hours}:${minutes}`;
};

// Simple markdown rendering utility
const renderMarkdown = (text: string) => {
  // Escape HTML
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Code blocks
  html = html.replace(/```([\s\S]*?)```/g, '<pre class="bg-black/50 p-3 rounded-lg overflow-x-auto mb-2 text-xs font-mono"><code>$1</code></pre>');

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code class="bg-black/30 px-1.5 py-0.5 rounded text-xs font-mono">$1</code>');

  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="font-bold">$1</strong>');
  html = html.replace(/__(.+?)__/g, '<strong class="font-bold">$1</strong>');

  // Italic
  html = html.replace(/\*(.+?)\*/g, '<em class="italic">$1</em>');
  html = html.replace(/_(.+?)_/g, '<em class="italic">$1</em>');

  // Headings
  html = html.replace(/^### (.+?)$/gm, '<h3 class="text-sm font-bold mb-1 mt-2">$1</h3>');
  html = html.replace(/^## (.+?)$/gm, '<h2 class="text-base font-bold mb-2 mt-2">$1</h2>');
  html = html.replace(/^# (.+?)$/gm, '<h1 class="text-lg font-bold mb-2 mt-3">$1</h1>');

  // Lists
  html = html.replace(/^- (.+?)$/gm, '<li class="ml-2">• $1</li>');
  html = html.replace(/(<li class="ml-2">.*<\/li>)/s, '<ul class="list-none mb-2 space-y-1">$1</ul>');

  // Line breaks
  html = html.replace(/\n/g, '<br />');

  return html;
};

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

interface ChatInterfaceProps {
  selectedModel: string;
  selectedBackend: "ollama" | "lmstudio";
  backendHealth: "healthy" | "unhealthy" | "checking";
}

export default function ChatInterface({
  selectedModel,
  selectedBackend,
  backendHealth,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "👋 Welcome to OCR-LLM Chat! I'm ready to help with your documents and questions. Upload a PDF or text file, or start asking questions!",
      timestamp: formatTime(new Date()),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [showFilePreview, setShowFilePreview] = useState(false);
  const [userScrolledUp, setUserScrolledUp] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (!userScrolledUp) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, userScrolledUp]);

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const container = e.currentTarget;
    const isAtBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight < 50;
    setUserScrolledUp(!isAtBottom);
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    if (backendHealth !== "healthy") {
      toast.error("Backend is not available. Please check your connection.");
      return;
    }

    if (!selectedModel) {
      toast.error("Please select a model first");
      return;
    }

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: formatTime(new Date()),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setUserScrolledUp(false);

    // Create abort controller for this request
    abortControllerRef.current = new AbortController();

    try {
      // Create query parameters for the API request
      const params = new URLSearchParams();
      params.append("message", input);
      params.append("model", selectedModel);
      params.append("backend", selectedBackend);

      const response = await fetch(`http://127.0.0.1:8000/api/chat?${params.toString()}`, {
        method: "POST",
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      // Handle streaming response
      const reader = response.body?.getReader();
      if (!reader) throw new Error("No response body");

      let assistantMessage = "";
      const assistantId = Date.now().toString();

      // Add empty assistant message
      setMessages((prev) => [
        ...prev,
        {
          id: assistantId,
          role: "assistant",
          content: "",
          timestamp: formatTime(new Date()),
        },
      ]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = new TextDecoder().decode(value);
        assistantMessage += chunk;

        // Update the last message
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1].content = assistantMessage;
          return updated;
        });
      }

      toast.success("Message processed successfully");
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        toast.info("Message generation stopped");
      } else {
        console.error("Error sending message:", error);
        toast.error(
          error instanceof Error ? error.message : "Failed to send message"
        );
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleStopGeneration = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsLoading(false);
      abortControllerRef.current = null;
      toast.info("Generation stopped");
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`http://127.0.0.1:8000/api/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setUploadedFile(data.content);
      setShowFilePreview(true);
      toast.success(`Document "${file.name}" uploaded successfully`);
    } catch (error) {
      console.error("Upload error:", error);
      toast.error("Failed to upload document");
    }
  };

  const clearMessages = () => {
    setMessages([
      {
        id: "1",
        role: "assistant",
        content:
          "👋 Welcome back! Chat cleared. Ready for a new conversation.",
        timestamp: formatTime(new Date()),
      },
    ]);
    setUploadedFile(null);
    setShowFilePreview(false);
  };

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-gradient-to-b from-slate-900 to-slate-900">
      {/* Messages Area */}
      <div 
        ref={messagesContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto px-6 py-6 space-y-4 [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-slate-700 [&::-webkit-scrollbar-thumb]:rounded-full hover:[&::-webkit-scrollbar-thumb]:bg-slate-600">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            } animate-in fade-in duration-300`}
          >
            <div
              className={`max-w-xl lg:max-w-2xl px-5 py-4 rounded-2xl ${
                message.role === "user"
                  ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-br-none shadow-lg shadow-indigo-500/30"
                  : "bg-slate-800/50 text-slate-100 border border-slate-700/50 rounded-bl-none"
              }`}
            >
              <div 
                className="text-sm leading-relaxed"
                dangerouslySetInnerHTML={{ __html: renderMarkdown(message.content) }}
              />
              <p
                className={`text-xs mt-2 ${
                  message.role === "user"
                    ? "text-indigo-100"
                    : "text-slate-500"
                }`}
              >
                {message.timestamp}
              </p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-800/50 text-slate-100 border border-slate-700/50 px-5 py-4 rounded-2xl rounded-bl-none flex gap-3">
              <Loader className="w-5 h-5 animate-spin text-indigo-400" />
              <span className="text-sm">Thinking...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* File Preview */}
      {showFilePreview && uploadedFile && (
        <div className="mx-6 mb-4 p-4 bg-slate-800/50 border border-slate-700/50 rounded-lg">
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-purple-400" />
              <span className="text-sm font-semibold text-slate-200">
                Document Loaded
              </span>
            </div>
            <button
              onClick={() => setShowFilePreview(false)}
              className="text-slate-400 hover:text-slate-200 transition"
            >
              ✕
            </button>
          </div>
          <p className="text-xs text-slate-400 line-clamp-2">
            {uploadedFile.substring(0, 150)}...
          </p>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-slate-700/50 bg-gradient-to-t from-slate-900 via-slate-900 to-slate-800 px-6 py-5">
        <form onSubmit={handleSendMessage} className="space-y-4">
          {/* File Upload Button */}
          <div className="flex gap-2">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt,.doc,.docx"
              onChange={handleFileUpload}
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="px-4 py-2 rounded-lg bg-slate-800/50 text-slate-300 hover:text-slate-100 hover:bg-slate-700/50 transition flex items-center gap-2 text-sm font-medium"
            >
              <Paperclip className="w-4 h-4" />
              Attach
            </button>

            <button
              type="button"
              onClick={clearMessages}
              className="px-4 py-2 rounded-lg bg-slate-800/50 text-slate-300 hover:text-slate-100 hover:bg-slate-700/50 transition flex items-center gap-2 text-sm font-medium"
            >
              <Trash2 className="w-4 h-4" />
              Clear
            </button>

            {isLoading && (
              <button
                type="button"
                onClick={handleStopGeneration}
                className="px-4 py-2 rounded-lg bg-red-500/20 text-red-300 hover:text-red-100 hover:bg-red-500/30 transition flex items-center gap-2 text-sm font-medium border border-red-500/30"
              >
                <Square className="w-4 h-4 fill-current" />
                Stop
              </button>
            )}
          </div>

          {/* Input Field */}
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                backendHealth === "healthy"
                  ? "Message your AI assistant..."
                  : "Backend offline..."
              }
              disabled={isLoading || backendHealth !== "healthy"}
              className="flex-1 px-5 py-3 rounded-lg bg-slate-800/50 border border-slate-700/50 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:ring-2 focus:ring-indigo-500/20 transition disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              type="submit"
              disabled={isLoading || backendHealth !== "healthy" || !input.trim()}
              className="px-6 py-3 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold hover:shadow-lg hover:shadow-indigo-500/50 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <Loader className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
