import { Link } from "react-router-dom";
import styles from "./DashboardHeader.module.scss";

const DashboardHeader: React.FC = () => {
  return (
    <nav className={styles.header}>
      <div className={styles.headerGroup}>
        <img className={styles.logo} src="/images/logo.png" />
        <div className={styles.menuItem}>Главная</div>
        {/* <div className={styles.menuItem}>Поддержка</div> */}
      </div>
      <div className={styles.headerGroup}>
        <Link to="/profile">
          <img src="/icons/User.svg" />
        </Link>
      </div>
    </nav>
  );
};

export default DashboardHeader;
