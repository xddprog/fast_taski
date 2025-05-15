// HomeRegistration.tsx
import { Link, useNavigate } from "react-router-dom"; // Добавляем useNavigate
import styles from "./HomeRegistration.module.scss";
import AuthButtons from "../AuthButtons/AuthButtons";
import { authWithVk, authWithYandex } from "../../utils/AuthWith";

const HomeRegistration: React.FC = () => {
  const navigate = useNavigate(); // Вызываем хук внутри компонента

  // Оборачиваем функции, чтобы передать navigate
  const handleVkAuth = (event: React.MouseEvent<HTMLButtonElement>) => {
    authWithVk(event, navigate);
  };

  const handleYandexAuth = (event: React.MouseEvent<HTMLButtonElement>) => {
    authWithYandex(event, navigate);
  };

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
        <AuthButtons
          yandexAuth={handleYandexAuth}
          vkauth={handleVkAuth}
        />
      </div>
    </section>
  );
};

export default HomeRegistration;