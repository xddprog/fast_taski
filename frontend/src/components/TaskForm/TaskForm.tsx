import styles from "./TaskForm.module.scss";

const TaskForm: React.FC = () => {
  return (
    <div className={styles.form}>
      <div className={styles.formTitle}>Основное</div>
      <label htmlFor="title">Название</label>
      <input
        id="title"
        type="text"
        name="title"
        placeholder="Заголовок задачи"
      ></input>
      <label htmlFor="description">Описание</label>
      <input
        id="description"
        type="text"
        name="description"
        placeholder="Текст задачи"
      ></input>
    </div>
  );
};

export default TaskForm;
