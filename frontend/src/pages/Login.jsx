import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const target = location.state?.from || "/";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login({ email, password });
      navigate(target, { replace: true });
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#ECE5DD] p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-2xl bg-white shadow-soft p-6 space-y-4">
        <h2 className="text-2xl font-semibold text-[#075E54]">Login</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded-lg border border-slate-300 p-3 focus:outline-none focus:ring-2 focus:ring-[#25D366]"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded-lg border border-slate-300 p-3 focus:outline-none focus:ring-2 focus:ring-[#25D366]"
          required
        />
        {error ? <p className="text-red-600 text-sm">{error}</p> : null}
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-[#25D366] py-3 font-semibold text-[#0b2b26] hover:brightness-95 transition"
        >
          {loading ? "Logging in..." : "Login"}
        </button>
        <p className="text-sm text-slate-600">
          No account?{" "}
          <Link className="text-[#075E54] font-medium" to="/signup">
            Create one
          </Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
