import { useState } from "react";
import { Link } from "react-router-dom";
import styles from "./Header.module.scss";

const Header: React.FC = () => {
  const [activeTab, setActiveTab] = useState("/");

  return (
    <header className={styles.header}>
      <div className={styles.leftHeaderBlock}>
        <div className={styles.imageContainer}>
          <img src="/icons/fastTaskiLogo.png" alt="fastTaskiLogo" />
        </div>
        <ul className={styles.hrefContainer}>
          <Link
            to="/"
            className={`${styles.headerHref} ${activeTab === "/" ? styles.active : ""}`}
            onClick={() => setActiveTab("/")}
          >
            Главная
          </Link>
          <Link
            to="/about"
            className={`${styles.headerHref} ${activeTab === "/about" ? styles.active : ""}`}
            onClick={() => setActiveTab("/about")}
          >
            О нас
          </Link>
          <Link
            to="/tarifs"
            className={`${styles.headerHref} ${activeTab === "/tarifs" ? styles.active : ""}`}
            onClick={() => setActiveTab("/tarifs")}
          >
            Тарифы
          </Link>
        </ul>
      </div>
      <div className={styles.rightHeaderBlock}>
        <button className={styles.helpButton}>Помощь</button>
        <Link to="/login" className={styles.registrationButton}>Вход</Link>
      </div>
    </header>
  );
};

export default Header;
