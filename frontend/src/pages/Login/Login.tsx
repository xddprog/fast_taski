// Login.tsx
import { Link } from "react-router-dom";
import styles from "./Login.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { useState } from "react";
import { loginUser } from "../../api/login/route";
import { useNavigate } from "react-router-dom";

const Login: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const navigate = useNavigate();

  async function login(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    try {
      const result = await loginUser(null, email, password);
      console.log("Вход успешен:", result);
      navigate("/profile");
    } catch (error) {
      console.error("Ошибка:", error);
    }
  }

  return (
    <>
      <Link to="/">
        <img className={styles.closeBtn} src="/icons/close.png" alt="Close" />
      </Link>
      <div className={styles.loginContainer}>
        <LoginForm
          title={"Войти"}
          login={email}
          pass={password}
          formType="login"
          handleLogin={login}
          handleEmail={setEmail}
          handlePass={setPassword}
        />
        <div className={styles.registrationText}>
          Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
        </div>
      </div>
    </>
  );
};

export default Login;
