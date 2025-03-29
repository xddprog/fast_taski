import { useNavigate } from "react-router-dom";
import styles from "./LoginForm.module.scss";
import { FormProps } from "../../types/form.ts";
import { FormEvent } from "react";

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
  const navigate = useNavigate();

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (formType === "register" && handleRegistre) {
      handleRegistre(event);
    } else if (handleLogin) {
      handleLogin(event);
    }
  };

  function authWithVk(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    window.location.assign(
      `${import.meta.env.VITE_VK_API_URL}?client_id=${
        import.meta.env.VITE_VK_APP_ID
      }` +
        `&display=popup` +
        `&redirect_uri=${encodeURIComponent(
          import.meta.env.VITE_REDIRECT_URI + "/auth/callback"
        )}` +
        `&response_type=code` +
        `&v=5.131`
    );
  }

  function authWithYandex(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    navigate("/auth/callback", { state: { service: "yandex", code: "123" } });
    window.location.assign(
      `${
        import.meta.env.VITE_YANDEX_API_URL
      }/authorize?response_type=token&client_id=${
        import.meta.env.VITE_YANDEX_CLIENT_ID
      }`
    );
  }

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
      <div className={styles.authOptions}>
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
          <button
            type="button"
            onClick={authWithVk}
            className={styles.authButton}
          >
            VK ID
          </button>
        </div>
      </div>
    </form>
  );
};

export default LoginForm;
