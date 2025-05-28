import DashboardHeader from "../components/DashboardHeader/DashboardHeader";
import DashboardNavbar from "../components/DashboardNavbar/DashboardNavbar";
import DashboardSettings from "../components/DashboardSettings/DashboardSettings";

const Settings: React.FC = () => {
  const style = {
    display: "flex",
  };

  return (
    <>
      <DashboardHeader />
      <div style={style}>
        <DashboardNavbar />
        <DashboardSettings />
      </div>
    </>
  );
};

export default Settings;
