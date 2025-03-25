import styles from "./HomeRegistration.module.scss";

const HomeRegistration: React.FC = () => {
  return (
    <section className={styles.homeRegistrationContainer}>
      <img
        className={styles.homeRegistrationImage}
        src="/images/homeRegistrationImage.png"
        alt="homeRegistrationImage"
      />
      <div className={styles.homeRegistrationPart}>
        <h1>Начинайте с Fast TASKI <br /> <span>прямо сейчас!</span></h1>
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
          <button className={styles.registrationButton}>Зарегистрироваться</button>
        </div>
        <div className={styles.otherVariant}>
          <h3>или продолжить с помощью</h3>
          <div className={styles.buttonContainer}>
            <button className={styles.yandexID}>Яндекс ID</button>
            <button className={styles.vkID}>VK ID</button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HomeRegistration;
