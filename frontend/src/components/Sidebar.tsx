"use client";

import { useState } from "react";
import {
  Settings,
  ChevronDown,
  Gauge,
  Radio,
} from "lucide-react";

interface SidebarProps {
  selectedBackend: "ollama" | "lmstudio";
  onBackendChange: (backend: "ollama" | "lmstudio") => void;
  models: string[];
  selectedModel: string;
  onModelChange: (model: string) => void;
  backendStatus: "healthy" | "unhealthy" | "checking";
}

export default function Sidebar({
  selectedBackend,
  onBackendChange,
  models,
  selectedModel,
  onModelChange,
  backendStatus,
}: SidebarProps) {
  const [expandedSections, setExpandedSections] = useState({
    backend: true,
    models: true,
    advanced: false,
  });

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  return (
    <div className="w-72 border-r border-slate-700/50 bg-gradient-to-b from-slate-900 via-slate-900 to-slate-800 flex flex-col overflow-hidden shadow-2xl">
      {/* Logo Section */}
      <div className="px-6 py-6 border-b border-slate-700/50">
        <div className="text-center">
          <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 mb-1">
            ◆
          </div>
          <h2 className="text-sm font-semibold text-slate-200">OCR-LLM</h2>
          <p className="text-xs text-slate-400 mt-1">Chat & Document Processing</p>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto">
        {/* Backend Selection */}
        <div className="px-4 py-4">
          <button
            onClick={() => toggleSection("backend")}
            className="w-full flex items-center justify-between mb-3 text-sm font-semibold text-slate-200 hover:text-slate-100 transition"
          >
            <div className="flex items-center gap-2">
              <Radio className="w-4 h-4 text-indigo-400" />
              Backend
            </div>
            <ChevronDown
              className={`w-4 h-4 transition ${
                expandedSections.backend ? "rotate-180" : ""
              }`}
            />
          </button>

          {expandedSections.backend && (
            <div className="space-y-2">
              {["ollama", "lmstudio"].map((backend) => (
                <button
                  key={backend}
                  onClick={() => onBackendChange(backend as "ollama" | "lmstudio")}
                  className={`w-full px-4 py-3 rounded-lg font-medium transition duration-200 text-left text-sm ${
                    selectedBackend === backend
                      ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg shadow-indigo-500/50"
                      : "bg-slate-800/50 text-slate-300 hover:bg-slate-700/50"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-2 h-2 rounded-full ${
                        selectedBackend === backend
                          ? "bg-white"
                          : "bg-slate-500"
                      }`}
                    ></div>
                    <span className="capitalize">
                      {backend === "lmstudio" ? "LMStudio" : "Ollama"}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Models Selection */}
        <div className="px-4 py-4 border-t border-slate-700/50">
          <button
            onClick={() => toggleSection("models")}
            className="w-full flex items-center justify-between mb-3 text-sm font-semibold text-slate-200 hover:text-slate-100 transition"
          >
            <div className="flex items-center gap-2">
              <Gauge className="w-4 h-4 text-purple-400" />
              Models
            </div>
            <ChevronDown
              className={`w-4 h-4 transition ${
                expandedSections.models ? "rotate-180" : ""
              }`}
            />
          </button>

          {expandedSections.models && (
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {models.length > 0 ? (
                models.map((model) => (
                  <button
                    key={model}
                    onClick={() => onModelChange(model)}
                    className={`w-full px-4 py-2 rounded-lg transition duration-200 text-left text-xs font-medium truncate ${
                      selectedModel === model
                        ? "bg-purple-500/20 border border-purple-500/50 text-purple-300"
                        : "bg-slate-800/50 text-slate-400 hover:bg-slate-700/50 hover:text-slate-300"
                    }`}
                    title={model}
                  >
                    {model}
                  </button>
                ))
              ) : (
                <div className="text-xs text-slate-500 py-4 text-center">
                  No models available
                </div>
              )}
            </div>
          )}
        </div>

        {/* Advanced Settings */}
        <div className="px-4 py-4 border-t border-slate-700/50">
          <button
            onClick={() => toggleSection("advanced")}
            className="w-full flex items-center justify-between mb-3 text-sm font-semibold text-slate-200 hover:text-slate-100 transition"
          >
            <div className="flex items-center gap-2">
              <Settings className="w-4 h-4 text-pink-400" />
              Advanced
            </div>
            <ChevronDown
              className={`w-4 h-4 transition ${
                expandedSections.advanced ? "rotate-180" : ""
              }`}
            />
          </button>

          {expandedSections.advanced && (
            <div className="space-y-4 p-4 bg-slate-800/30 rounded-lg border border-slate-700/50">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-2">
                  Temperature
                </label>
                <input
                  type="range"
                  min="0"
                  max="2"
                  step="0.1"
                  defaultValue="0.7"
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                />
                <p className="text-xs text-slate-500 mt-1">Controls randomness</p>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-2">
                  Top P
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  defaultValue="0.9"
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
                <p className="text-xs text-slate-500 mt-1">Nucleus sampling</p>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-2">
                  Top K
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="1"
                  defaultValue="40"
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-pink-500"
                />
                <p className="text-xs text-slate-500 mt-1">Token selection</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-slate-700/50 px-4 py-4 bg-slate-900/50">
        <p className="text-xs text-slate-500 text-center">
          {backendStatus === "healthy" ? (
            <span className="text-green-400">✓ Backend Connected</span>
          ) : backendStatus === "checking" ? (
            <span className="text-yellow-400">• Checking...</span>
          ) : (
            <span className="text-red-400">✗ Backend Offline</span>
          )}
        </p>
      </div>
    </div>
  );
}
