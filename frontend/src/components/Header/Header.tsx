import { useEffect, useRef, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import styles from "./Header.module.scss";

const Header: React.FC = () => {
  const [activeTab, setActiveTab] = useState("/");
  const [isActive, setIsActive] = useState(false);

  const menuRef = useRef<HTMLDivElement>(null);
  const burgerButtonRef = useRef<HTMLButtonElement>(null);
  const location = useLocation();

  useEffect(() => {
    setActiveTab(location.pathname);
  }, [location]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target as Node) &&
        burgerButtonRef.current &&
        !burgerButtonRef.current.contains(event.target as Node)
      ) {
        setIsActive(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    if (isActive) {
      document.body.classList.add("no-scroll");
    } else {
      document.body.classList.remove("no-scroll");
    }
  }, [isActive]);

  const handleBurgerLinkClick = (path: string) => {
    setActiveTab(path);
    setIsActive(false);
  };

  return (
    <>
      <header className={styles.header}>
        <div className={styles.leftHeaderBlock}>
          <div className={styles.imageContainer}>
            <img src="/icons/fastTaskiLogo.png" alt="fastTaskiLogo" />
          </div>
          <ul className={styles.hrefContainer}>
            <Link
              to="/"
              className={`${styles.headerHref} ${
                activeTab === "/" ? styles.active : ""
              }`}
              onClick={() => setActiveTab("/")}
            >
              Главная
            </Link>
            <Link
              to="/about"
              className={`${styles.headerHref} ${
                activeTab === "/about" ? styles.active : ""
              }`}
              onClick={() => setActiveTab("/about")}
            >
              О нас
            </Link>
            <Link
              to="/tarifs"
              className={`${styles.headerHref} ${
                activeTab === "/tarifs" ? styles.active : ""
              }`}
              onClick={() => setActiveTab("/tarifs")}
            >
              Тарифы
            </Link>
          </ul>
        </div>
        <div className={`${styles.burgerMenu} ${isActive ? styles.active : ""}`}>
          <button
            className={styles.burgerButton}
            onClick={() => setIsActive(!isActive)}
            ref={burgerButtonRef}
          >
            {isActive ? (
              <img src="/icons/activeBurgerMenu.png" alt="Close Menu" />
            ) : (
              <img src="/icons/burgerMenu.png" alt="Open Menu" />
            )}
          </button>

          <nav
            className={`${styles.menu} ${isActive ? styles.activeMenu : ""}`}
            ref={menuRef}
          >
            <div className={styles.menuContent}>
              <img src="/icons/fastTaskiLogo.png" alt="fastTaskiLogo" />
              <div className={styles.mainPartOfLinks}>
                <Link
                  to="/"
                  className={`${styles.headerHref} ${
                    activeTab === "/" ? styles.active : ""
                  }`}
                  onClick={() => handleBurgerLinkClick("/")}
                >
                  Главная
                </Link>
                <Link
                  to="/about"
                  className={`${styles.headerHref} ${
                    activeTab === "/about" ? styles.active : ""
                  }`}
                  onClick={() => handleBurgerLinkClick("/about")}
                >
                  О нас
                </Link>
                <Link
                  to="/tarifs"
                  className={`${styles.headerHref} ${
                    activeTab === "/tarifs" ? styles.active : ""
                  }`}
                  onClick={() => handleBurgerLinkClick("/tarifs")}
                >
                  Тарифы
                </Link>
              </div>
              <hr />
              <Link
                to="/help"
                className={`${styles.headerHref} ${
                  activeTab === "/help" ? styles.active : ""
                }`}
                onClick={() => handleBurgerLinkClick("/help")}
              >
                Помощь
              </Link>
            </div>
          </nav>
        </div>
        <div className={styles.rightHeaderBlock}>
          <button className={styles.helpButton}>Помощь</button>
          <Link to="/login" className={styles.registrationButton}>
            Вход
          </Link>
        </div>
      </header>
      {isActive && <div className={styles.overlay}></div>}
    </>
  );
};

export default Header;