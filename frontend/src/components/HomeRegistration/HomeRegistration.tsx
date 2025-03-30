import { Link } from "react-router-dom";
import styles from "./HomeRegistration.module.scss";
import AuthButtons from "../AuthButtons/AuthButtons";

const HomeRegistration: React.FC = () => {
  return (
    <section className={styles.homeRegistrationContainer}>
      <img
        className={styles.homeRegistrationImage}
        src="/images/homeRegistrationImage.png"
        alt="homeRegistrationImage"
      />
      <div className={styles.homeRegistrationPart}>
        <h1>
          Начинайте с Fast TASKI <br /> <span>прямо сейчас</span>!
        </h1>
        <div className={styles.homeRegistrationForm}>
          <div className={styles.registrationInputContainer}>
            <label>Почта</label>
            <input
              type="email"
              id="email"
              className={styles.inputForRegistration}
              placeholder="Введите вашу почту"
            />
          </div>
          <Link to="/register" className={styles.registrationButton}>
            Зарегистрироваться
          </Link>
        </div>
        <AuthButtons />
      </div>
    </section>
  );
};

export default HomeRegistration;
