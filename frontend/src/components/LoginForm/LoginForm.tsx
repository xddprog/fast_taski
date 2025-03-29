import { useNavigate } from "react-router-dom";
import styles from "./LoginForm.module.scss";
import { FormEvent } from "react";

interface FormProps {
  title: string;
  formType?: string;
  handleLogin?: (event: FormEvent<HTMLFormElement>) => void;
  handleRegistre?: (event: FormEvent<HTMLFormElement>) => void;
}

const LoginForm: React.FC<FormProps> = ({
  title,
  formType,
  handleLogin,
  handleRegistre,
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
      `${import.meta.env.VITE_VK_API_URL}?client_id=${import.meta.env.VITE_VK_APP_ID}` +
        `&display=popup` +
        `&redirect_uri=${encodeURIComponent(import.meta.env.VITE_REDIRECT_URI + "/auth/callback")}` +
        `&response_type=code` +
        `&v=5.131`
    );
  }

  function authWithYandex(event: React.MouseEvent<HTMLButtonElement>) {
    navigate("/auth/callback", { state: { service: "yandex", code: "123" } });
    event.preventDefault();
    window.location.assign(
      `${import.meta.env.VITE_YANDEX_API_URL}/authorize?response_type=token&client_id=${
        import.meta.env.VITE_YANDEX_CLIENT_ID
      }`
    );
  }

  return (
    <form className={styles.loginForm} onSubmit={handleSubmit}>
      <h1>{title}</h1>
      <label htmlFor="email">Почта</label>
      <input type="text" id="email" name="email" placeholder="mail@mail.mail" />
      {formType === "register" && (
        <>
          <label htmlFor="username">Имя пользователя</label>
          <input type="text" id="username" name="username" placeholder="username" />
        </>
      )}
      <label htmlFor="password">Пароль</label>
      <input
        type="password"
        id="password"
        name="password"
        placeholder="Пароль"
      />
      {formType === "register" ? (
        <>
          <label htmlFor="password_repeat">Повторите пароль</label>
          <input
            type="password"
            id="password_repeat"
            name="password_repeat"
            placeholder="Повторите пароль"
          />
          <button type="submit">Продолжить</button>
        </>
      ) : (
        <button type="submit">Продолжить</button>
      )}
      <div style={{ display: "flex", flexDirection: "column" }}>
        <p
          style={{
            color: "#fff",
            fontSize: 12,
            marginBottom: 10,
            textAlign: "center",
          }}
        >
          Или {formType === "register" ? "зарегистрируйтесь" : "войдите"} с помощью
        </p>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 10, margin: 0 }}>
          <button
            type="button"
            onClick={authWithYandex}
            style={{ backgroundColor: "#fff", color: "#000", width: "100%", margin: 0 }}
          >
            Яндекс ID
          </button>
          <button
            type="button"
            onClick={authWithVk}
            style={{ backgroundColor: "#fff", color: "#000", width: "100%", margin: 0 }}
          >
            VK ID
          </button>
        </div>
      </div>
    </form>
  );
};

export default LoginForm;