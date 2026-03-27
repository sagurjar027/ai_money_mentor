import { useState } from "react";
import api from "../api";
import LoadingSpinner from "../components/LoadingSpinner";

const starterQuestions = [
  "How should I split my monthly salary between spending, saving, and investing?",
  "What is the difference between an emergency fund and regular savings?",
  "How can I start investing as a beginner in India?",
];

function ChatHelper() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submitQuestion = async (nextQuestion) => {
    const trimmedQuestion = nextQuestion.trim();
    if (!trimmedQuestion) {
      setError("Please enter a question first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const { data } = await api.post("/chat", { question: trimmedQuestion });
      setAnswer(data.answer);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to get a response right now.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await submitQuestion(question);
  };

  const handleStarterClick = async (starterQuestion) => {
    setQuestion(starterQuestion);
    await submitQuestion(starterQuestion);
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold">Chat Helper</h2>
        <p className="text-sm text-slate-600">
          Ask a general question and get a simple AI-generated answer.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="glass-card space-y-4">
        <label className="block text-sm text-slate-600">
          Your question
          <textarea
            rows="5"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: How much of my income should I keep in an emergency fund?"
            className="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />
        </label>
        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-indigo-600 px-4 py-3 text-white font-medium hover:bg-indigo-700 transition-colors disabled:cursor-not-allowed disabled:opacity-70"
        >
          Ask Question
        </button>
      </form>

      <div className="glass-card">
        <h3 className="text-lg font-semibold mb-3">Try these</h3>
        <div className="flex flex-wrap gap-3">
          {starterQuestions.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => handleStarterClick(item)}
              disabled={loading}
              className="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-900 transition-colors hover:bg-emerald-100 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      {loading ? <LoadingSpinner label="Thinking through your question..." /> : null}
      {error ? <p className="text-red-600">{error}</p> : null}

      {answer ? (
        <div className="glass-card space-y-3">
          <h3 className="text-lg font-semibold">Answer</h3>
          <div className="chat-bubble whitespace-pre-wrap">{answer}</div>
        </div>
      ) : null}
    </div>
  );
}

export default ChatHelper;
