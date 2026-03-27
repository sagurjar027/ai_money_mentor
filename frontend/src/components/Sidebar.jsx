import { NavLink } from "react-router-dom";
import { useAuth } from "../auth";

const navItems = [
  { label: "Health Score", path: "/" },
  { label: "Chat Helper", path: "/chat" },
  { label: "FIRE Planner", path: "/fire" },
  { label: "SIP Calculator", path: "/sip" },
  { label: "Tax Calculator", path: "/tax" },
];

function Sidebar() {
  const { user, isAdmin, logout } = useAuth();
  return (
    <aside className="w-full md:w-72 bg-[#075E54] text-white p-5 md:min-h-screen">
      <h1 className="text-xl font-bold mb-2">AI Money Mentor</h1>
      <p className="text-sm text-emerald-100 mb-6">Hi {user?.full_name}</p>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block w-full text-left px-4 py-3 rounded-xl transition-all ${
                isActive ? "bg-[#25D366] text-[#0b2b26] font-semibold" : "text-emerald-50 hover:bg-[#0b7b6f]"
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
        {isAdmin ? (
          <NavLink
            to="/admin"
            className={({ isActive }) =>
              `block w-full text-left px-4 py-3 rounded-xl transition-all ${
                isActive ? "bg-[#25D366] text-[#0b2b26] font-semibold" : "text-emerald-50 hover:bg-[#0b7b6f]"
              }`
            }
          >
            Admin Dashboard
          </NavLink>
        ) : null}
      </nav>
      <button
        onClick={logout}
        className="mt-8 w-full rounded-xl bg-white/15 px-4 py-3 text-left hover:bg-white/25 transition-colors"
      >
        Logout
      </button>
      <div className="mt-4 rounded-xl bg-white/10 p-4 text-sm text-emerald-50">
        Role: {user?.role === "admin" ? "Admin" : "User"}
      </div>
    </aside>
  );
}

export default Sidebar;
