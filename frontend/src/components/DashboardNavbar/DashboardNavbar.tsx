import { NavLink } from "react-router-dom";
import NavbarGroup from "../NavbarGroup/NavbarGroup";
import styles from "./DashboardNavbar.module.scss";

const DashboardNavbar: React.FC = () => {
  return (
    <nav className={styles.navbar}>
      <section className={styles.navSection}>
        <div className={styles.group}>
          <div className={styles.titleGroup}>Команды</div>
          <NavbarGroup />

          <NavLink
            to="/settings"
            className={({ isActive }) =>
              isActive ? styles.navItemActive : styles.navItem
            }
          >
            <span className={`${styles.icon} ${styles.gear}`}></span>
            <span>Управление</span>
          </NavLink>
        </div>

        <div>
          <div className={styles.titleGroup}>Дашборд</div>
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive ? styles.navItemActive : styles.navItem
            }
          >
            <span className={`${styles.icon} ${styles.list}`}></span>
            <span>Задачи</span>
          </NavLink>
        </div>
      </section>

      <section className={styles.navSection}>
        <NavLink
          to="/profile"
          className={({ isActive }) =>
            isActive ? styles.navItemActive : styles.navItem
          }
        >
          <span className={`${styles.icon} ${styles.user}`}></span>
          <span>Профиль</span>
        </NavLink>
      </section>
    </nav>
  );
};

export default DashboardNavbar;
