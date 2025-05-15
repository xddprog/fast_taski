import Task from "../Task/Task";
import styles from "./TasksContainer.module.scss";

const tasksList = [
  {
    id: 1,
    columnCategory: "Новые задачи",
    tasks: [
      {
        task_id: 1,
        tag: "tag",
        title: "title",
        text: "some text",
        people: "people",
        comments: ["1", "2", "3"],
      },
    ],
  },
  {
    id: 2,
    columnCategory: "В работе",
    tasks: [
      {
        task_id: 1,
        tag: "tag",
        title: "title",
        text: "some text",
        people: "people",
        comments: ["1", "2", "3"],
      },
    ],
  },
];

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
      <div className={styles.tasksContainer}>
        <Task tasksList={tasksList}></Task>
      </div>
    </section>
  );
};

export default TasksContainer;
