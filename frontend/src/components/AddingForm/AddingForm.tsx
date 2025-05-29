import styles from "./AddingForm.module.scss";

type Props = {
  title: string;
  text: string;
  onClick: (param: string) => void;
};

const AddingForm: React.FC<Props> = ({ title, text, onClick }) => {
  return (
    <div className={styles.overlay} onClick={() => onClick("close")}>
      <div className={styles.addingForm}>
        <div className={styles.formHeading}>
          <div className={styles.formTitle}>{title}</div>
          <img src="icons/Cross.svg" onClick={() => onClick("close")} />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor={text}>{text}</label>
          <input id={text} type="text" name={text} placeholder={title} />
        </div>
        <button>Сохранить</button>
      </div>
    </div>
  );
};

export default AddingForm;
