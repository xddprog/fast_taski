import styles from "./SettingsForm.module.scss";

const SettingsForm: React.FC = () => {
  return (
    <section className={styles.settingsForm}>
      <div className={styles.settingsGroup}>
        <div className={styles.settingsGroupLine}>
          <span>Столбцы</span>
          <img src="/icons/plus.svg" />
        </div>
        <div className={styles.settingsContainer}>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              <div className={styles.squer}></div>
              <span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              <div className={styles.squer}></div>
              <span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              <div className={styles.squer}></div>
              <span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              <div className={styles.squer}></div>
              <span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
        </div>
      </div>

      <div className={styles.settingsGroup}>
        <div className={styles.settingsGroupLine}>
          <span>Тэги</span>
          <img src="/icons/plus.svg" />
        </div>
        <div className={styles.settingsContainer}>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              #<span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              #<span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              #<span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnSettingsCard}>
            <div className={styles.columnSettingsCardLine}>
              #<span>Новые задачи</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
        </div>
      </div>

      <button className={styles.btn}>Сохранить</button>
    </section>
  );
};

export default SettingsForm;
