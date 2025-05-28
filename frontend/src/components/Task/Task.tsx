import { useState } from "react";
import styles from "./Task.module.scss";
import FiltersFrom from "../FiltersFrom/FiltersFrom";
import TaskForm from "../TaskForm/TaskForm";

interface TaskProps {
  tasksList: {
    id: number;
    columnCategory: string;
    tasks: {
      tag: string;
      title: string;
      text: string;
      people: string;
      comments: Array<string>;
    }[];
  }[];
}

const Task: React.FC<TaskProps> = ({ tasksList }) => {
  const [activeTaskForm, setAactiveTaskForm] = useState(false);

  function handleFormActions() {
    setAactiveTaskForm(!activeTaskForm);
  }

  return (
    <>
      {activeTaskForm ? (
        <div className={styles.overlay} onClick={() => handleFormActions()}>
          <div className={styles.popup} onClick={(e) => e.stopPropagation()}>
            <div className={styles.popupHeader}>
              <div className={styles.title}>Создание задачи</div>
              <img src="/icons/Cross.svg" onClick={() => handleFormActions()} />
            </div>
            <TaskForm />
            <FiltersFrom />
          </div>
        </div>
      ) : (
        <></>
      )}

      {tasksList.map((taskColumn) => (
        <div key={taskColumn.id} className={styles.taskColumn}>
          <div className={styles.taskColumnHeader}>
            <h1>
              {taskColumn.columnCategory} <span>{taskColumn.tasks.length}</span>
            </h1>
            <img src="icons/plus.svg" onClick={() => handleFormActions()} />
          </div>
          {taskColumn.tasks.map((task) => (
            <div key={task.title} className={styles.taskCard}>
              <h3>{task.tag}</h3>
              <h2>{task.title}</h2>
              <p>{task.text}</p>
            </div>
          ))}
        </div>
      ))}
    </>
  );
};

export default Task;
