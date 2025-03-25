import { Link } from "react-router-dom";
import styles from "./Login.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { useState } from "react";
import SuccessBunner from "../../components/SuccessBanner/SuccessBunner";

const Login: React.FC = () => {
  const [success, setSuccess] = useState(false);
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  function login() {
    setSuccess(true);
  }

  return (
    <>
      <Link to="/">
        <img className={styles.closeBtn} src="/icons/close.png" />
      </Link>
      <div className={styles.loginContainer}>
        {success ? (
          <SuccessBunner
            description={"Вы успешно вошли в аккаунт"}
          ></SuccessBunner>
        ) : (
          <>
            <LoginForm
              title={"Войти"}
              login={email}
              pass={password}
              handleLogin={login}
              handleEmail={setEmail}
              handlePass={setPassword}
            ></LoginForm>
            <div className={styles.registrationText}>
              Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default Login;
