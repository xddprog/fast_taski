import styles from "./AboutPanel.module.scss";

const AboutPanel: React.FC = () => {
  return (
    <section className={styles.aboutPanelBlock}>
      <div className={styles.aboutPanelText}>
        <h1 className={styles.longTitle}>Наша команда</h1>
        <h1 className={styles.forAdaptive}>Команда</h1>
        <p>
          Наша продуктовая команда работает вместе уже более двух лет Проект
        </p>
        <br />
        <p>
          Fast TASKI — наша общая идея, которой горит каждый участник команды
        </p>
      </div>
      <div className={styles.supportBlock}>
        <div className={styles.supportBlockText}>
          <h1>Служба поддержки</h1>
          <p>
            Наши специалисты технической поддержки
            <br />
            готовы оперативно помочь
            <br />с любыми возникшими вопросами
          </p>
        </div>
        <button>Поддержка</button>
        <img src="/images/aboutPanel_img.png" />
      </div>
    </section>
  );
};

export default AboutPanel;
