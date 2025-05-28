import styles from "./FiltersFrom.module.scss";

const FiltersFrom: React.FC = () => {
  return (
    <section className={styles.filtersForm}>
      <div className={styles.filtersGroup}>
        <div className={styles.filtersGroupLine}>
          <span>Тэги</span>
          <div className={styles.filtersDrop}>Очистить</div>
        </div>
        <div className={styles.filtersContainer}>
          <div className={styles.columnfiltersCard}>
            <div className={styles.columnfiltersCardLine}>
              <input type="checkbox" />#<span>Тэг</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnfiltersCard}>
            <div className={styles.columnfiltersCardLine}>
              <input type="checkbox" />#<span>Тэг</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnfiltersCard}>
            <div className={styles.columnfiltersCardLine}>
              <input type="checkbox" />#<span>Тэг</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
          <div className={styles.columnfiltersCard}>
            <div className={styles.columnfiltersCardLine}>
              <input type="checkbox" />#<span>Тэг</span>
            </div>
            <img src="/icons/Trash.svg" />
          </div>
        </div>
      </div>

      <button className={styles.btn}>Сохранить</button>
    </section>
  );
};

export default FiltersFrom;
