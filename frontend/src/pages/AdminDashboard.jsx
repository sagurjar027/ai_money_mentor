import { useEffect, useState } from "react";
import api from "../api";
import LoadingSpinner from "../components/LoadingSpinner";

function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadUsers = async () => {
    setLoading(true);
    setError("");
    try {
      const { data } = await api.get("/admin/users");
      setUsers(data.users || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to fetch users.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const toggleUser = async (userId, isActive) => {
    try {
      await api.patch(`/admin/users/${userId}/status`, { is_active: !isActive });
      setUsers((prev) =>
        prev.map((u) => (u.id === userId ? { ...u, is_active: !isActive } : u))
      );
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update user status.");
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Admin Dashboard</h2>
      <div className="glass-card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">All Users</h3>
          <button onClick={loadUsers} className="rounded-lg bg-slate-900 text-white px-3 py-2 text-sm">
            Refresh
          </button>
        </div>
        {loading ? <LoadingSpinner label="Loading users..." /> : null}
        {error ? <p className="text-red-600 text-sm mb-3">{error}</p> : null}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left border-b border-slate-200">
                <th className="py-2">Name</th>
                <th className="py-2">Email</th>
                <th className="py-2">Role</th>
                <th className="py-2">Status</th>
                <th className="py-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b border-slate-100">
                  <td className="py-3">{u.full_name}</td>
                  <td className="py-3">{u.email}</td>
                  <td className="py-3 capitalize">{u.role}</td>
                  <td className="py-3">{u.is_active ? "Active" : "Disabled"}</td>
                  <td className="py-3">
                    <button
                      onClick={() => toggleUser(u.id, u.is_active)}
                      className={`rounded-lg px-3 py-1 text-xs font-medium ${
                        u.is_active ? "bg-red-100 text-red-700" : "bg-emerald-100 text-emerald-700"
                      }`}
                    >
                      {u.is_active ? "Disable" : "Enable"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
