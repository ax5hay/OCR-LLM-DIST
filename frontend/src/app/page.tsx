"use client";

import { useState, useEffect, useRef } from "react";
import { Toaster } from "sonner";
import ChatInterface from "@/components/ChatInterface";
import Sidebar from "@/components/Sidebar";
import { AlertCircle, Zap } from "lucide-react";

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<"healthy" | "unhealthy" | "checking">("checking");
  const [selectedBackend, setSelectedBackend] = useState<"ollama" | "lmstudio">("lmstudio");
  const [models, setModels] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>("");
  const statusCheckRef = useRef<NodeJS.Timeout | null>(null);

  // Check backend health on mount and when backend changes
  useEffect(() => {
    const checkHealth = async () => {
      try {
        setBackendStatus("checking");
        const response = await fetch(`http://127.0.0.1:8000/api/health?backend=${selectedBackend}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
        
        if (response.ok) {
          setBackendStatus("healthy");
          // Fetch available models
          const modelsResponse = await fetch(`http://127.0.0.1:8000/api/models?backend=${selectedBackend}`);
          if (modelsResponse.ok) {
            const data = await modelsResponse.json();
            setModels(data.models || []);
            if (data.models && data.models.length > 0 && !selectedModel) {
              setSelectedModel(data.models[0]);
            }
          }
        } else {
          setBackendStatus("unhealthy");
        }
      } catch (error) {
        console.error("Health check failed:", error);
        setBackendStatus("unhealthy");
      }
    };

    checkHealth();
    // Recheck every 30 seconds
    statusCheckRef.current = setInterval(checkHealth, 30000);

    return () => {
      if (statusCheckRef.current) clearInterval(statusCheckRef.current);
    };
  }, [selectedBackend, selectedModel]);

  return (
    <>
      <Toaster position="top-right" richColors theme="dark" />
      <div className="flex h-full w-full gap-0">
        {/* Sidebar */}
        <Sidebar
          selectedBackend={selectedBackend}
          onBackendChange={setSelectedBackend}
          models={models}
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
          backendStatus={backendStatus}
        />

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="border-b border-slate-700/50 bg-gradient-to-r from-slate-900 to-slate-800 px-6 py-4 shadow-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg blur opacity-75 animate-pulse"></div>
                  <div className="relative bg-slate-900 px-4 py-2 rounded-lg">
                    <Zap className="w-5 h-5 text-indigo-400" />
                  </div>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
                    OCR-LLM Chat
                  </h1>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Powered by {selectedModel ? `${selectedModel}` : "AI"} on {selectedBackend}
                  </p>
                </div>
              </div>

              {/* Backend Status */}
              <div className="flex items-center gap-2">
                {backendStatus === "checking" && (
                  <div className="text-xs text-slate-400 flex items-center gap-2">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                    Checking...
                  </div>
                )}
                {backendStatus === "healthy" && (
                  <div className="text-xs text-green-400 flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                    Connected
                  </div>
                )}
                {backendStatus === "unhealthy" && (
                  <div className="text-xs text-red-400 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4" />
                    Offline
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Chat Area */}
          <ChatInterface
            selectedModel={selectedModel}
            selectedBackend={selectedBackend}
            backendHealth={backendStatus}
          />
        </div>
      </div>
    </>
  );
}
