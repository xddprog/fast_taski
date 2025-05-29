import styles from "./LoginForm.module.scss";
import { FormProps } from "../../types/form.ts";
import { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import AuthButtons from "../AuthButtons/AuthButtons.tsx";
import { authWithVk, authWithYandex } from "../../utils/AuthWith.ts";

const LoginForm: React.FC<FormProps> = ({
  login,
  pass,
  passRep,
  title,
  formType,
  handleLogin,
  handleRegistre,
  handleEmail,
  handlePass,
  handlePassRep,
}) => {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (formType === "register" && handleRegistre) {
      handleRegistre(event);
      console.log(import.meta.env.VITE_BASE_API_URL);
    } else if (handleLogin) {
      handleLogin(event);
    }
  };

  const navigate = useNavigate();

  //   function authWithYandex(event: React.MouseEvent<HTMLButtonElement>) {
  //     event.preventDefault();
  //     window.location.assign(
  //       `${import.meta.env.VITE_YANDEX_API_URL}/authorize?response_type=token&client_id=${
  //         import.meta.env.VITE_YANDEX_CLIENT_ID
  //       }`
  //     );
  //   }

  const handleVkAuth = (event: React.MouseEvent<HTMLButtonElement>) => {
    authWithVk(event, navigate);
  };

  const handleYandexAuth = (event: React.MouseEvent<HTMLButtonElement>) => {
    authWithYandex(event, navigate);
  };

  return (
    <form className={styles.loginForm} onSubmit={handleSubmit}>
      <h1>{title}</h1>
      <label htmlFor="email">Почта</label>
      <input
        type="text"
        id="email"
        name="email"
        placeholder="mail@mail.mail"
        value={login}
        onChange={(e) => handleEmail?.(e.target.value)}
      />
      {formType === "register" && (
        <>
          <label htmlFor="username">Имя пользователя</label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="username"
          />
        </>
      )}
      <label htmlFor="password">Пароль</label>
      <input
        type="password"
        id="password"
        name="password"
        placeholder="Пароль"
        value={pass}
        onChange={(e) => handlePass?.(e.target.value)}
      />
      {formType === "register" && (
        <>
          <label htmlFor="password_repeat">Повторите пароль</label>
          <input
            type="password"
            id="password_repeat"
            name="password_repeat"
            placeholder="Повторите пароль"
            value={passRep}
            onChange={(e) => handlePassRep?.(e.target.value)}
          />
        </>
      )}
      <button type="submit" className={styles.continueBtn}>
        Продолжить
      </button>
      {/* <div className={styles.authOptions}>
        <p className={styles.authText}>
          Или {formType === "register" ? "зарегистрируйтесь" : "войдите"} с
          помощью
        </p>
        <div className={styles.authButtons}>
          <button
            type="button"
            onClick={authWithYandex}
            className={styles.authButton}
          >
            Яндекс ID
          </button>
          <button type="button" onClick={} className={styles.authButton}>
            VK ID
          </button>
        </div>
      </div> */}
      <AuthButtons yandexAuth={handleYandexAuth} vkauth={handleVkAuth} />
    </form>
  );
};

export default LoginForm;
