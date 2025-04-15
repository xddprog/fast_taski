import NavbarGroup from "../NavbarGroup/NavbarGroup";
import styles from "./DashboardNavbar.module.scss";

const groups = [
  {
    icons: ["icons/tasks.png", "icons/tasks.png"],
    labels: ["Мои задачи", "Мой календарь"],
  },
  {
    title: "Команды",
    icons: ["icons/tasks.png"],
    labels: ["Управление"],
  },
  {
    title: "Дэшборд",
    icons: [
      "icons/tasks.png",
      "icons/tasks.png",
      "icons/tasks.png",
      "icons/tasks.png",
    ],
    labels: ["Задачи", "Календарь", "Заметки", "Статистика"],
  },
];

const DashboardNavbar: React.FC = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.personLine}>
        <img src="images/Avatar.png" alt="avatar" />
        <p>Nickname</p>
        <img className={styles.logoutBtn} src="icons/logout.png" alt="logout" />
      </div>
      {groups.map((item, index) => (
        <NavbarGroup key={index} item={item} />
      ))}
    </nav>
  );
};

export default DashboardNavbar;
