import DashboardNavbar from "../components/DashboardNavbar/DashboardNavbar";
import ProfileContainer from "../components/ProfileContainer/ProfileContainer";

const Profile: React.FC = () => {
    const style = {
        display: "flex",
    };

    return (
        <div style={style}>
            <DashboardNavbar />
            <ProfileContainer />
        </div>
    );
};

export default Profile;
