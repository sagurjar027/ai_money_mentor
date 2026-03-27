function MetricCard({ label, value, subValue }) {
  return (
    <div className="glass-card">
      <p className="text-sm text-slate-500">{label}</p>
      <h3 className="text-2xl font-semibold mt-2">{value}</h3>
      {subValue ? <p className="text-sm text-slate-500 mt-1">{subValue}</p> : null}
    </div>
  );
}

export default MetricCard;
