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
            type="password_repeat"
            id="password_repeat"
            name="password_repeat"
            placeholder="Повторите пароль"
          />
          <button onClick={handleRegistre}>Продолжить</button>
        </>
      ) : (
        <button onClick={handleLogin}>Продолжить</button>
      )}
    </form>
  );
};

export default LoginForm;
