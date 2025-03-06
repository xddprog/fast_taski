import HomeRegistration from "../components/HomeRegistration/HomeRegistration";
import Info from "../components/Info/Info";
import Panels from "../components/Panels/Panels";

const Home: React.FC = () => {
  return (
    <>
      <Info />
      <Panels />
      <HomeRegistration />
    </>
  );
};

export default Home;
