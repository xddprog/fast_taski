import { Link } from "react-router-dom";
import styles from "./Login.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { FormEvent, useState } from "react";
import SuccessBunner from "../../components/SuccessBanner/SuccessBunner";
import AuthService from "../../api/services/authService";
import { LoginUserInterface } from "../../interfaces/authInterfaces";

const Login: React.FC = () => {
  const [success, setSuccess] = useState(false);
  const authService = new AuthService();

  async function login(event: FormEvent<HTMLFormElement>) {
    const formData = new FormData(event.currentTarget);
    const loginData: LoginUserInterface = {
      email: formData.get("email") as string,
      password: formData.get("password") as string,
    };

    await authService.loginUser(loginData).then(res => {
      console.log(res);
    });
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
            <LoginForm title={"Войти"} handleLogin={login} formType="login"></LoginForm>
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
