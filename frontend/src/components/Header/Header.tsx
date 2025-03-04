import styles from "./Header.module.scss";

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.leftHeaderBlock}>
        <div className={styles.imageContainer}>
          <img src="/icons/fastTaskiLogo.png" alt="fastTaskiLogo" />
        </div>
        <ul className={styles.hrefContainer}>
          <a href="" className={styles.headerHref}>
            Главная
          </a>
          <a href="" className={styles.headerHref}>
            О нас
          </a>
          <a href="" className={styles.headerHref}>
            Тарифы
          </a>
        </ul>
      </div>
      <div className={styles.rightHeaderBlock}>
        <button className={styles.helpButton}>Помощь</button>
        <button className={styles.registrationButton}>Вход</button>
      </div>
    </header>
  );
};

export default Header;
