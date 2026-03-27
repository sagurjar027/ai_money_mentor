import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth";

function Signup() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await signup({ full_name: fullName, email, password, role });
      navigate("/", { replace: true });
    } catch (err) {
      setError(err?.response?.data?.detail || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#ECE5DD] p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-2xl bg-white shadow-soft p-6 space-y-4">
        <h2 className="text-2xl font-semibold text-[#075E54]">Signup</h2>
        <input
          type="text"
          placeholder="Full name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="w-full rounded-lg border border-slate-300 p-3 focus:outline-none focus:ring-2 focus:ring-[#25D366]"
          required
        />
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
        <label className="text-sm text-slate-600">
          Profile Type
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="mt-1 w-full rounded-lg border border-slate-300 p-3 focus:outline-none focus:ring-2 focus:ring-[#25D366]"
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </label>
        {error ? <p className="text-red-600 text-sm">{error}</p> : null}
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-[#25D366] py-3 font-semibold text-[#0b2b26] hover:brightness-95 transition"
        >
          {loading ? "Creating account..." : "Create account"}
        </button>
        <p className="text-sm text-slate-600">
          Already have account?{" "}
          <Link className="text-[#075E54] font-medium" to="/login">
            Login
          </Link>
        </p>
      </form>
    </div>
  );
}

export default Signup;
