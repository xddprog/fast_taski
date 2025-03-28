import styles from "./LoginForm.module.scss";

interface FormProps {
  title: string;
  formType?: string;
  handleLogin?: () => void;
  handleRegistre?: () => void;
}

const LoginForm: React.FC<FormProps> = ({
  title,
  formType,
  handleLogin,
  handleRegistre,
}) => {
  function authWithVk(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    window.location.assign(
        `${import.meta.env.VITE_VK_API_URL}?client_id=${import.meta.env.VITE_VK_APP_ID}`
        + `&display=popup`
        + `&redirect_uri=${encodeURIComponent(import.meta.env.VITE_REDIRECT_URI + '/auth/callback')}`
        + `&response_type=code`
        + `&v=5.131`
    );
  }


  function authWithYandex(event: React.FormEvent<HTMLFormElement>) {
      event.preventDefault();
      window.location.assign(
          `${import.meta.env.VITE_YANDEX_API_URL}/authorize?response_type=token&client_id=${import.meta.env.VITE_YANDEX_CLIENT_ID}`);
  }

  return (
    <form className={styles.loginForm}>
      <h1>{title}</h1>
      <label htmlFor="email">Почта</label>
      <input type="text" id="email" name="email" placeholder="mail@mail.mail" />
      <label htmlFor="password">Пароль</label>
      <input
        type="password"
        id="password"
        name="password"
        placeholder="Пароль"
      />
      {formType === "register" ? (
        <>
          <label htmlFor="password">Повторите пароль</label>
          <input
            type="password"
            id="password_repeat"
            name="password_repeat"
            placeholder="Повторите пароль"
          />
          <button onClick={handleRegistre}>Продолжить</button>
        </>
      ) : (
        <button onClick={handleLogin}>Продолжить</button>
      )}
      <div style={{ display: "flex", flexDirection: "column" }}>
        <p style={{color: "#fff", fontSize: 12, marginBottom: 10, width: "100%", textAlign: "center"}}>
          Или {formType == "regster" ? "зарегистрируйтесь": "войдите"} с помощью
        </p>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 10, margin: 0 }}>
          <button
            onClick={authWithYandex} 
            style={{ backgroundColor: "#fff", color: "#000", width: "100%", margin: 0 }}
          >
            Яндекс ID
          </button>
          <button 
            onClick={authWithVk}
            style={{ backgroundColor: "#fff", color: "#000", width: "100%", margin: 0 }}>VK ID
          </button>
        </div>
      </div>
    </form>
  );
};

export default LoginForm;
