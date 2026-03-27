import { useState } from "react";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../api";
import LoadingSpinner from "../components/LoadingSpinner";
import MetricCard from "../components/MetricCard";

const initialForm = {
  salary: 1200000,
  investments_80c: 100000,
  deductions: 50000,
};

function TaxCalculator() {
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
      const { data } = await api.post("/tax_calc", form);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to calculate tax.");
    } finally {
      setLoading(false);
    }
  };

  const chartData = result
    ? [
        { regime: "Old Regime", tax: result.tax_old },
        { regime: "New Regime", tax: result.tax_new },
      ]
    : [];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Tax Calculator</h2>

      <form onSubmit={submit} className="glass-card grid grid-cols-1 md:grid-cols-3 gap-4">
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
          className="md:col-span-3 rounded-xl bg-indigo-600 px-4 py-3 text-white font-medium hover:bg-indigo-700 transition-colors"
        >
          Compare Tax Regimes
        </button>
      </form>

      {loading ? <LoadingSpinner label="Computing tax options..." /> : null}
      {error ? <p className="text-red-600">{error}</p> : null}

      {result ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricCard label="Old Regime Tax" value={`INR ${result.tax_old.toLocaleString()}`} />
            <MetricCard label="New Regime Tax" value={`INR ${result.tax_new.toLocaleString()}`} />
            <MetricCard label="Best Regime" value={result.best_regime} />
          </div>

          <div className="glass-card h-72">
            <h3 className="text-lg font-semibold mb-4">Tax Comparison</h3>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <XAxis dataKey="regime" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="tax" fill="#22c55e" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="glass-card">
              <h3 className="text-lg font-semibold mb-3">Suggestions</h3>
              <ul className="list-disc list-inside text-sm text-slate-700 space-y-2">
                {result.suggestions.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="glass-card">
              <h3 className="text-lg font-semibold mb-3">AI Advice</h3>
              <div className="chat-bubble whitespace-pre-wrap">
                {result.ai_advice}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default TaxCalculator;
