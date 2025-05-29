import { Link, useNavigate } from "react-router-dom";
import styles from "./Login.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { FormEvent, useState } from "react";
import SuccessBunner from "../../components/SuccessBanner/SuccessBunner";
import AuthService from "../../api/services/authService";
import { LoginUserInterface } from "../../interfaces/authInterfaces";

const Login: React.FC = () => {
  const [success, setSuccess] = useState(false);
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const navigate = useNavigate();
  const authService = new AuthService();

  async function login(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const loginData: LoginUserInterface = {
      email: formData.get("email") as string,
      password: formData.get("password") as string,
    };

    try {
      const res = await authService.loginUser(loginData);
      console.log("Вход успешен:", res);
      setSuccess(true);
      setTimeout(() => {
        navigate("/dashboard");
      }, 2000);
    } catch (error) {
      console.error("Ошибка:", error);
      alert("Ошибка при входе. Проверьте данные.");
    }
  }

  return (
    <>
      <Link to="/">
        <img className={styles.closeBtn} src="/icons/close.png" alt="Close" />
      </Link>
      <div className={styles.loginContainer}>
        {success ? (
          <SuccessBunner />
        ) : (
          <>
            <LoginForm
              title={"Войти"}
              formType="login"
              handleLogin={login}
              login={email}
              pass={password}
              handleEmail={setEmail}
              handlePass={setPassword}
            />
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
