function LoadingSpinner({ label = "Loading..." }) {
  return (
    <div className="flex items-center gap-3 text-slate-600">
      <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
      <span>{label}</span>
    </div>
  );
}

export default LoadingSpinner;
