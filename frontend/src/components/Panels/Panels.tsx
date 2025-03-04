import styles from "./Panels.module.scss";

const Panels: React.FC = () => {
  return (
    <section className={styles.PanelsContainer}>
      <div className={styles.firstRow}>
        <div className={styles.leftBlockInFirstRow}>
          <img src="/images/leftBlockImage.png" alt="leftBlockImage" />
          <div className={styles.leftBlockText}>
            <h1>Работайте эффективнее <br />— достигайте большего!</h1>
            <h3>
              Наша платформа позволяет управлять задачами, <br />
              что повышыет эффективность команды <br /> 
              и кажого её участника по отдельности!
            </h3>
          </div>
          <button className={styles.leftBlockButton}>Начать бесплатно</button>
        </div>
        <div className={styles.rightBlockInFirstRow}>
          <div className={styles.rightBlockUpperText}>
            <h1>Скидки в честь запуска</h1>
            <h2>
              В честь запуска платформы Fast TASKI, мы предоставляем скидку на
              все тарифыв размере 42%
            </h2>
          </div>
          <h3 className={styles.rightBlockSaleText}>
            Акция продлится до 30.04.2025
          </h3>
        </div>
      </div>
      <div className={styles.secondRow}>
        <div className={styles.leftBlockInSecondRow}></div>
        <div className={styles.rightBlockInSecondRow}></div>
      </div>
    </section>
  );
};

export default Panels;
