import { useState } from "react";
import Task from "../Task/Task";
import styles from "./TasksContainer.module.scss";
import SettingsForm from "../SettingsForm/SettingsForm";
import FiltersFrom from "../FiltersFrom/FiltersFrom";
import AddingForm from "../AddingForm/AddingForm";

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
  const [activeAddingForm, setActiveAddingForm] = useState("");

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

  function handleAddingFormClick(param: string) {
    switch (param) {
      case "column":
        setActiveAddingForm("column");
        break;

      case "tag":
        setActiveAddingForm("tag");
        break;
      case "close":
        setActiveAddingForm("");
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
            <SettingsForm onClick={handleAddingFormClick} />
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

      {activeAddingForm === "column" ? (
        <AddingForm
          title={"Новый столбец"}
          text={"Название"}
          onClick={handleAddingFormClick}
        />
      ) : activeAddingForm === "tag" ? (
        <AddingForm
          title={"Новый тэг"}
          text={"Тэг"}
          onClick={handleAddingFormClick}
        />
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
