import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

function AppLayout() {
  return (
    <div className="min-h-screen bg-[#ECE5DD] md:flex">
      <Sidebar />
      <main className="flex-1 p-5 md:p-8">
        <div className="rounded-2xl border border-slate-100 bg-white p-4 md:p-6 shadow-soft">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

export default AppLayout;
