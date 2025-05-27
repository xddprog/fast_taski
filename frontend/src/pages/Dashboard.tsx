import DashboardHeader from "../components/DashboardHeader/DashboardHeader";
import DashboardNavbar from "../components/DashboardNavbar/DashboardNavbar";
import TasksContainer from "../components/TasksContainer/TasksContainer";

const Dashboard: React.FC = () => {
  const style = {
    display: "flex",
  };

  return (
    <>
      <DashboardHeader />
      <div style={style}>
        <DashboardNavbar />
        <TasksContainer />
      </div>
    </>
  );
};

export default Dashboard;
