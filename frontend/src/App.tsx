import Header from "./components/Header/Header";
import Home from "./pages/Home";
import About from "./pages/About";
import Tarifs from "./pages/Tarifs";
import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import Profile from "./pages/Profile";
import Dashboard from "./pages/Dashboard";
import Footer from "./components/Footer/Footer";
import { Routes, Route, useLocation } from "react-router-dom";

const App: React.FC = () => {
  const location = useLocation();
  const hideHeaderFooter =
    location.pathname === "/login" ||
    location.pathname === "/register" ||
    location.pathname === "/dashboard";
  return (
    <>
      {!hideHeaderFooter && <Header />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/tarifs" element={<Tarifs />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* <Route path="*" element={<NotFound />} />{" "} */}
        {/* 404 - для всех несуществующих путей */}
      </Routes>
      {!hideHeaderFooter && <Footer />}
    </>
  );
};

export default App;
