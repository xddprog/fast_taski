import { Link } from "react-router-dom";
import styles from "./Panels.module.scss";

const Panels: React.FC = () => {
  return (
    <section className={styles.PanelsContainer}>
      <div className={styles.firstRow}>
        <div className={styles.leftBlockInFirstRow}>
          <img src="/images/leftBlockImage.png" alt="leftBlockImage" />
          <div className={styles.leftBlockText}>
            <h1>
              Работайте эффективнее <br />— достигайте большего!
            </h1>
            <h3>
              Наша платформа позволяет управлять задачами, <br />
              что повышыет эффективность команды <br />и кажого её участника по
              отдельности!
            </h3>
          </div>
          <Link to="/register" className={styles.leftBlockButton}>
            Начать бесплатно
          </Link>
        </div>
        <div className={styles.rightBlockInFirstRow}>
          <div className={styles.rightBlockUpperText}>
            <h1>Скидки в честь запуска</h1>
            <h2>
              В честь запуска платформы Fast TASKI, мы предоставляем скидку на
              все тарифы <br /> в размере 42%
            </h2>
          </div>
          <h3 className={styles.rightBlockSaleText}>
            Акция продлится до 30.04.2025
          </h3>
          <h3 className={styles.rightBlockSaleTextPhone}>
            Акция продлится до 30.04.2025
          </h3>
        </div>
      </div>
      <div className={styles.secondRow}>
        <div className={styles.leftBlockInSecondRow}>
          <h1>Мы поддерживаем интеграции</h1>
          <h3>
            С помощью Fast TASKI можно получать статусы задач через коммиты на
            GitHub, а уведомленияо них будут приходить прямо в Telegram
          </h3>
        </div>
        <div className={styles.rightBlockInSecondRow}>
          <img src="/images/rightBlockImage.png" alt="aiImage" />
          <div className={styles.aiTextBlock}>
            <h1>Помощь от ИИ</h1>
            <div className={styles.containerForLi}>
              <h3>Благодаря нашему умному помощнику вы сможете:</h3>
              <br />
              <ul>
                <li>Оптимизировать распределение задач</li>
                <li>Автоматизировать генерацию отчётов</li>
              </ul>
            </div>
          </div>
          <h3 className={styles.underTextAboutTarif}>
            Доступно при любом тарифе
          </h3>
        </div>
      </div>
      <div className={styles.mediumDisplay}>
      <div className={styles.leftBlockInFirstRow}>
          <img src="/images/leftBlockImage.png" alt="leftBlockImage" />
          <div className={styles.leftBlockText}>
            <h1>
              Работайте эффективнее <br />— достигайте большего!
            </h1>
            <h3>
              Наша платформа позволяет управлять задачами, <br />
              что повышыет эффективность команды <br />и кажого её участника по
              отдельности!
            </h3>
          </div>
          <Link to="/register" className={styles.leftBlockButton}>
            Начать бесплатно
          </Link>
        </div>
        <div className={styles.centralBlock}>
          <div className={styles.leftBlockInSecondRow}>
            <h1>Мы поддерживаем интеграции</h1>
            <h3>
              С помощью Fast TASKI можно получать статусы задач через коммиты на
              GitHub, а уведомленияо них будут приходить прямо в Telegram
            </h3>
          </div>
          <div className={styles.rightBlockInFirstRow}>
            <div className={styles.rightBlockUpperText}>
              <h1>Скидки в честь запуска</h1>
              <h2>
                В честь запуска платформы Fast TASKI, мы предоставляем скидку на
                все тарифы <br /> в размере 42%
              </h2>
            </div>
            <h3 className={styles.rightBlockSaleText}>
              Акция продлится до 30.04.2025
            </h3>
          </div>
        </div>
        <div className={styles.rightBlockInSecondRow}>
          <img src="/images/rightBlockImage.png" alt="aiImage" />
          <div className={styles.aiTextBlock}>
            <h1>Помощь от ИИ</h1>
            <div className={styles.containerForLi}>
              <h3>Благодаря нашему умному помощнику вы сможете:</h3>
              <br />
              <ul>
                <li>Оптимизировать распределение задач</li>
                <li>Автоматизировать генерацию отчётов</li>
              </ul>
            </div>
          </div>
          <h3 className={styles.underTextAboutTarif}>
            Доступно при любом тарифе
          </h3>
        </div>
      </div>
    </section>
  );
};

export default Panels;
