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

  function handleSettingsClick() {
    setActiveSettingsForm(true);
  }

  function handleCloseSettings() {
    setActiveSettingsForm(false);
  }

  function handleFiltersClick() {
    setActiveFilterForm(true);
  }

  function handleCloseFilters() {
    setActiveFilterForm(false);
  }

  return (
    <>
      {activeSettingsForm ? (
        <div className={styles.overlay} onClick={handleCloseSettings}>
          <div className={styles.popup} onClick={(e) => e.stopPropagation()}>
            <div className={styles.popupHeader}>
              <div className={styles.title}>Доска задач</div>
              <img src="/icons/Cross.svg" onClick={handleCloseSettings} />
            </div>
            <SettingsForm />
          </div>
        </div>
      ) : (
        <></>
      )}

      {activeFilterForm ? (
        <div className={styles.overlay} onClick={handleCloseFilters}>
          <div className={styles.popup} onClick={(e) => e.stopPropagation()}>
            <div className={styles.popupHeader}>
              <div className={styles.title}>Фильтры</div>
              <img src="/icons/Cross.svg" onClick={handleCloseFilters} />
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
            <button onClick={() => handleSettingsClick()}>
              <img src={"/icons/Gear.svg"} alt="settings" />
            </button>
            <button onClick={() => handleFiltersClick()}>
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
