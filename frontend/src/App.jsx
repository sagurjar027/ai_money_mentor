import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth";
import AppLayout from "./components/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard";
import ChatHelper from "./pages/ChatHelper";
import FirePlanner from "./pages/FirePlanner";
import HealthScore from "./pages/HealthScore";
import Login from "./pages/Login";
import SipCalculator from "./pages/SipCalculator";
import Signup from "./pages/Signup";
import TaxCalculator from "./pages/TaxCalculator";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<HealthScore />} />
            <Route path="/chat" element={<ChatHelper />} />
            <Route path="/fire" element={<FirePlanner />} />
            <Route path="/sip" element={<SipCalculator />} />
            <Route path="/tax" element={<TaxCalculator />} />
            <Route
              path="/admin"
              element={
                <ProtectedRoute adminOnly>
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
