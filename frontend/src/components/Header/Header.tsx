import { Link } from "react-router-dom";
import styles from "./Header.module.scss";

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.leftHeaderBlock}>
        <div className={styles.imageContainer}>
          <img src="/icons/fastTaskiLogo.png" alt="fastTaskiLogo" />
        </div>
        <ul className={styles.hrefContainer}>
          <Link to="/" className={styles.headerHref}>
            Главная
          </Link>
          <Link to="/about" className={styles.headerHref}>
            О нас
          </Link>
          <Link to="/" className={styles.headerHref}>
            Тарифы
          </Link>
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
