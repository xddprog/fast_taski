import styles from "./AboutText.module.scss";

const AboutText: React.FC = () => {
  return (
    <section className={styles.aboutBlock}>
      <div className={styles.aboutText}>
        <h1>Подробнее о нас</h1>
        <p>
          Создаём <span>универсальное</span> решение в сфере управления
        </p>
      </div>
      <img src="/images/about_img.png" />
    </section>
  );
};

export default AboutText;
