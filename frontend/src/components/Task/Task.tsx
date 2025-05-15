import styles from "./Task.module.scss";

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
  return (
    <>
      {tasksList.map((taskColumn) => (
        <div key={taskColumn.id} className={styles.taskColumn}>
          <div className={styles.taskColumnHeader}>
            <h1>
              {taskColumn.columnCategory} <span>{taskColumn.tasks.length}</span>
            </h1>
            <img src="icons/plus.png" />
          </div>
          {taskColumn.tasks.map((task) => (
            <div key={task.title} className={styles.taskCard}>
              <h3>{task.tag}</h3>
              <h2>{task.title}</h2>
              <p>{task.text}</p>
              <div className={styles.taskCardComments}>
                <span>{task.comments.length}</span>
                <img src="icons/comment.png" />
              </div>
            </div>
          ))}
        </div>
      ))}
    </>
  );
};

export default Task;
