import styles from "./TasksContainer.module.scss";

const TasksContainer: React.FC = () => {
  return (
    <section className={styles.dashboard}>
      <div className={styles.dashboardTools}>
        <h1>Задачи</h1>
        <div className={styles.toolsBtns}>
          <button>
            <img src={"/icons/settings.png"} alt="settings" />
          </button>
          <button>
            <img src={"/icons/filter.png"} alt="settings" />
            <span>Фильтры</span>
          </button>
        </div>
      </div>
      <div className={styles.tasksContainer}></div>
    </section>
  );
};

export default TasksContainer;
