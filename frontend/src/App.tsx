// import Header from "./components/Header/Header";
// import Info from "./components/Info/Info";
// import Panels from "./components/Panels/Panels";
import Home from "./pages/Home";
import About from "./pages/About";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";

const App: React.FC = () => {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        {/* <Route path="*" element={<NotFound />} />{" "} */}
        {/* 404 - для всех несуществующих путей */}
      </Routes>
      <Footer />
    </>
  );
};

export default App;
