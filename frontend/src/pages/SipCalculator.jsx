import { useState } from "react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../api";
import LoadingSpinner from "../components/LoadingSpinner";
import MetricCard from "../components/MetricCard";

const initialForm = {
  monthly_investment: 10000,
  years: 10,
  expected_annual_return: 12,
  current_savings: 50000,
};

function SipCalculator() {
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
      const { data } = await api.post("/sip_calc", form);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to calculate SIP projection.");
    } finally {
      setLoading(false);
    }
  };

  const chartData = [];
  if (result) {
    const monthlyRate = form.expected_annual_return / 100 / 12;
    for (let year = 0; year <= form.years; year += 1) {
      const months = year * 12;
      const investedAmount = form.monthly_investment * months + form.current_savings;
      let projectedValue = investedAmount;

      if (months > 0 && monthlyRate > 0) {
        const futureValueSip =
          form.monthly_investment * (((1 + monthlyRate) ** months - 1) / monthlyRate) * (1 + monthlyRate);
        const futureValueLumpSum = form.current_savings * ((1 + monthlyRate) ** months);
        projectedValue = futureValueSip + futureValueLumpSum;
      }

      chartData.push({
        year,
        invested: Math.round(investedAmount),
        value: Math.round(projectedValue),
      });
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">SIP Calculator</h2>

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
          Calculate SIP Growth
        </button>
      </form>

      {loading ? <LoadingSpinner label="Projecting your SIP growth..." /> : null}
      {error ? <p className="text-red-600">{error}</p> : null}

      {result ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <MetricCard label="Projected Value" value={`INR ${result.estimated_value.toLocaleString()}`} />
            <MetricCard label="Total Invested" value={`INR ${result.total_invested.toLocaleString()}`} />
            <MetricCard label="Estimated Gains" value={`INR ${result.estimated_gains.toLocaleString()}`} />
            <MetricCard label="Wealth Multiple" value={`${result.wealth_multiplier}x`} />
          </div>

          <div className="glass-card">
            <h3 className="text-lg font-semibold mb-2">Plan Outlook</h3>
            <p className="text-slate-700">{result.outlook}</p>
          </div>

          <div className="glass-card h-80">
            <h3 className="text-lg font-semibold mb-4">Projected Growth</h3>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="invested" stackId="1" stroke="#94a3b8" fill="#cbd5e1" />
                <Area type="monotone" dataKey="value" stackId="2" stroke="#4f46e5" fill="#818cf8" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="glass-card">
            <h3 className="text-lg font-semibold mb-3">AI Advice</h3>
            <div className="chat-bubble whitespace-pre-wrap">{result.ai_advice}</div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default SipCalculator;
