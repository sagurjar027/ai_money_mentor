import { useState } from "react";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../api";
import LoadingSpinner from "../components/LoadingSpinner";
import MetricCard from "../components/MetricCard";

const initialForm = {
  age: 28,
  income: 100000,
  expenses: 50000,
  savings: 400000,
  retirement_age: 50,
};

function FirePlanner() {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const onChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: Number(value) }));
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const { data } = await api.post("/fire_plan", form);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to generate FIRE plan.");
    } finally {
      setLoading(false);
    }
  };

  const projection = [];
  if (result) {
    let corpus = form.savings;
    const years = Math.max(result.years_left, 1);
    for (let year = 0; year <= years; year += 1) {
      projection.push({ year, corpus: Math.round(corpus) });
      corpus = (corpus + result.monthly_sip * 12) * 1.1;
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">FIRE Planner</h2>

      <form onSubmit={submit} className="glass-card grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(form).map(([key, value]) => (
          <label key={key} className="text-sm text-slate-600">
            {key.replaceAll("_", " ").toUpperCase()}
            <input
              type="number"
              min="0"
              value={value}
              onChange={(e) => onChange(key, e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </label>
        ))}
        <button
          type="submit"
          className="md:col-span-2 rounded-xl bg-indigo-600 px-4 py-3 text-white font-medium hover:bg-indigo-700 transition-colors"
        >
          Generate FIRE Plan
        </button>
      </form>

      {loading ? <LoadingSpinner label="Building your FIRE roadmap..." /> : null}
      {error ? <p className="text-red-600">{error}</p> : null}

      {result ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricCard label="Target Corpus" value={`INR ${result.target_corpus.toLocaleString()}`} />
            <MetricCard label="Monthly SIP" value={`INR ${result.monthly_sip.toLocaleString()}`} />
            <MetricCard label="Years Left" value={result.years_left} />
          </div>

          <div className="glass-card">
            <h3 className="text-lg font-semibold mb-2">Investment Strategy</h3>
            <p className="text-slate-700">{result.investment_strategy}</p>
          </div>

          <div className="glass-card h-80">
            <h3 className="text-lg font-semibold mb-4">Projected Investment Growth</h3>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={projection}>
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="corpus" stroke="#4f46e5" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="glass-card">
            <h3 className="text-lg font-semibold mb-3">AI Advice</h3>
            <div className="chat-bubble whitespace-pre-wrap">
              {result.ai_advice}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default FirePlanner;
