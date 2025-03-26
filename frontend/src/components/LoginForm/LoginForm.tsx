import styles from "./LoginForm.module.scss";
import { FormProps } from "../../types/form.ts";
import AuthButtons from "../AuthButtons/AuthButtons.tsx";

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
  return (
    <form
      className={styles.loginForm}
      onSubmit={formType === "register" ? handleRegistre : handleLogin}
    >
      <h1>{title}</h1>
      <label htmlFor="email">Почта</label>
      <input
        type="text"
        id="email"
        name="email"
        placeholder="mail@mail.mail"
        value={login}
        onChange={(e) => {
          handleEmail(e.target.value);
        }}
      />
      <label htmlFor="password">Пароль</label>
      <input
        type="password"
        id="password"
        name="password"
        placeholder="Пароль"
        value={pass}
        onChange={(e) => {
          if (handlePass) {
            handlePass(e.target.value);
          }
        }}
      />
      {formType === "register" ? (
        <>
          <label htmlFor="password">Повторите пароль</label>
          <input
            type="password"
            id="password_repeat"
            name="password_repeat"
            placeholder="Повторите пароль"
            value={passRep}
            onChange={(e) => {
              if (handlePassRep) {
                handlePassRep(e.target.value);
              }
            }}
          />
        </>
      ) : (
        <></>
      )}
      <button className={styles.continueBtn} type="submit">
        Продолжить
      </button>
      <AuthButtons></AuthButtons>
    </form>
  );
};

export default LoginForm;
