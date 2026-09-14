import { SendHorizontal, Sparkles } from "lucide-react";
import { useState } from "react";
import { api } from "../services/api";

const prompts = [
  "Why is Router R5 unstable?",
  "Which router is most likely to fail?",
  "Summarize today's incidents.",
  "What should I do about packet loss?"
];

export default function Copilot() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Ask me about router instability, predicted failures, packet loss, incidents, or NOC actions."
    }
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  async function send(text = input) {
    const clean = text.trim();
    if (!clean || busy) return;
    setBusy(true);
    setMessages((items) => [...items, { role: "user", content: clean }]);
    setInput("");
    try {
      const response = await api.chat(clean);
      setMessages((items) => [
        ...items,
        {
          role: "assistant",
          content: response.analysis,
          detail: response
        }
      ]);
    } catch (error) {
      setMessages((items) => [...items, { role: "assistant", content: error.message }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto max-w-5xl">
      <section className="rounded border border-line bg-panel">
        <div className="flex items-center gap-3 border-b border-line p-4">
          <div className="grid h-10 w-10 place-items-center rounded bg-cyan/15 text-cyan">
            <Sparkles size={20} />
          </div>
          <div>
            <h3 className="font-semibold">AI Copilot Chat</h3>
            <p className="text-sm text-slate-400">Offline deterministic NOC assistant with Gemini adapter boundary.</p>
          </div>
        </div>

        <div className="h-[58vh] space-y-4 overflow-y-auto p-4">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[82%] rounded border p-4 ${message.role === "user" ? "border-cyan/40 bg-cyan/10" : "border-line bg-slate-950/45"}`}>
                <p className="text-sm leading-6">{message.content}</p>
                {message.detail && (
                  <div className="mt-3 space-y-3 border-t border-line pt-3 text-sm text-slate-300">
                    <p><span className="font-semibold text-slate-100">Explanation:</span> {message.detail.explanation}</p>
                    <div>
                      <p className="font-semibold text-slate-100">Recommendations</p>
                      <ul className="mt-1 list-disc space-y-1 pl-5">
                        {message.detail.recommendations.map((item) => <li key={item}>{item}</li>)}
                      </ul>
                    </div>
                    <div>
                      <p className="font-semibold text-slate-100">Evidence</p>
                      <ul className="mt-1 list-disc space-y-1 pl-5">
                        {message.detail.evidence.map((item) => <li key={item}>{item}</li>)}
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="border-t border-line p-4">
          <div className="mb-3 flex flex-wrap gap-2">
            {prompts.map((prompt) => (
              <button key={prompt} onClick={() => send(prompt)} className="rounded border border-line px-3 py-2 text-sm text-slate-300 hover:border-cyan hover:text-cyan">
                {prompt}
              </button>
            ))}
          </div>
          <form
            className="flex gap-3"
            onSubmit={(event) => {
              event.preventDefault();
              send();
            }}
          >
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask the copilot..."
              className="min-w-0 flex-1 rounded border border-line bg-slate-950 px-4 py-3 text-sm outline-none focus:border-cyan"
            />
            <button className="grid h-12 w-12 place-items-center rounded bg-cyan text-slate-950 disabled:opacity-50" disabled={busy}>
              <SendHorizontal size={20} />
            </button>
          </form>
        </div>
      </section>
    </div>
  );
}
