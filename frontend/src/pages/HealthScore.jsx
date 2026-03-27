import { useState } from "react";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../api";
import LoadingSpinner from "../components/LoadingSpinner";
import MetricCard from "../components/MetricCard";

const initialForm = {
  age: 28,
  monthly_income: 80000,
  monthly_expenses: 45000,
  savings: 250000,
  debt: 8000,
  investments: 12000,
  insurance: 6000000,
};

function HealthScore() {
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
      const { data } = await api.post("/health_score", form);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to calculate health score.");
    } finally {
      setLoading(false);
    }
  };

  const breakdown = result?.breakdown
    ? [
        { name: "Emergency", value: result.breakdown.emergency_score },
        { name: "Debt", value: result.breakdown.debt_score },
        { name: "Investment", value: result.breakdown.investment_score },
        { name: "Insurance", value: result.breakdown.insurance_score },
        { name: "Discipline", value: result.breakdown.discipline_score },
      ]
    : [];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Money Health Score</h2>

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
          Calculate Score
        </button>
      </form>

      {loading ? <LoadingSpinner label="Calculating score..." /> : null}
      {error ? <p className="text-red-600">{error}</p> : null}

      {result ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricCard label="Score" value={`${result.score}/100`} subValue={result.category} />
            <div className="glass-card md:col-span-2">
              <p className="text-sm text-slate-500 mb-2">Progress</p>
              <div className="h-3 rounded-full bg-slate-100 overflow-hidden">
                <div
                  className="h-full bg-indigo-500 transition-all duration-500"
                  style={{ width: `${Math.min(Math.max(result.score, 0), 100)}%` }}
                />
              </div>
            </div>
          </div>

          <div className="glass-card h-80">
            <h3 className="text-lg font-semibold mb-4">Score Breakdown</h3>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={breakdown}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#6366f1" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="glass-card">
              <h3 className="text-lg font-semibold mb-3">Insights</h3>
              <div className="space-y-2">
                {result.insights.map((item) => (
                  <div key={item} className="rounded-lg border border-slate-200 p-3 text-sm">
                    {item}
                  </div>
                ))}
              </div>
            </div>
            <div className="glass-card">
              <h3 className="text-lg font-semibold mb-3">AI Advice</h3>
              <div className="chat-bubble whitespace-pre-wrap">
                {result.ai_advice}
              </div>
              <h4 className="font-medium mt-4 mb-2">Recommendations</h4>
              <ul className="list-disc list-inside text-sm text-slate-700 space-y-1">
                {result.recommendations.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default HealthScore;
