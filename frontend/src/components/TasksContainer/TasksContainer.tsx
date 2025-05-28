import { useState } from "react";
import Task from "../Task/Task";
import styles from "./TasksContainer.module.scss";
import SettingsForm from "../SettingsForm/SettingsForm";
import FiltersFrom from "../FiltersFrom/FiltersFrom";

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
  const [activeSettingsForm, setActiveSettingsForm] = useState(false);
  const [activeFilterForm, setActiveFilterForm] = useState(false);

  function handleActionForm(param: string) {
    switch (param) {
      case "settings":
        setActiveSettingsForm(!activeSettingsForm);
        break;

      case "filter":
        setActiveFilterForm(!activeFilterForm);
        break;
    }
  }

  return (
    <>
      {activeSettingsForm ? (
        <div
          className={styles.overlay}
          onClick={() => handleActionForm("settings")}
        >
          <div className={styles.popup} onClick={(e) => e.stopPropagation()}>
            <div className={styles.popupHeader}>
              <div className={styles.title}>Доска задач</div>
              <img
                src="/icons/Cross.svg"
                onClick={() => handleActionForm("settings")}
              />
            </div>
            <SettingsForm />
          </div>
        </div>
      ) : (
        <></>
      )}

      {activeFilterForm ? (
        <div
          className={styles.overlay}
          onClick={() => handleActionForm("filter")}
        >
          <div className={styles.popup} onClick={(e) => e.stopPropagation()}>
            <div className={styles.popupHeader}>
              <div className={styles.title}>Фильтры</div>
              <img
                src="/icons/Cross.svg"
                onClick={() => handleActionForm("filter")}
              />
            </div>
            <FiltersFrom />
          </div>
        </div>
      ) : (
        <></>
      )}

      <section className={styles.dashboard}>
        <div className={styles.dashboardTools}>
          <h1>Задачи</h1>
          <div className={styles.toolsBtns}>
            <button onClick={() => handleActionForm("settings")}>
              <img src={"/icons/Gear.svg"} alt="settings" />
            </button>
            <button onClick={() => handleActionForm("filter")}>
              <img src={"/icons/filter.png"} alt="settings" />
              <span>Фильтры</span>
            </button>
          </div>
        </div>
        <div className={styles.tasksContainer}>
          <Task tasksList={tasksList}></Task>
        </div>
      </section>
    </>
  );
};

export default TasksContainer;
