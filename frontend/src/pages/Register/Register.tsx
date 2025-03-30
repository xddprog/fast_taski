import { Link } from "react-router-dom";
import styles from "./Register.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { useState } from "react";
import SuccessBunner from "../../components/SuccessBanner/SuccessBunner";
import { registerUser } from "../../api/register/route";

const Register: React.FC = () => {
  const [success, setSuccess] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [passwordRepeat, setPasswordRepeat] = useState<string>("");
  // const [code, setCode] = useState<string>("");

  function registre(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (password !== passwordRepeat) {
      alert("Пароли не совпадают");
    } else {
      setSuccess(true);
    }
  }

  async function verify(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    try {
      const result = await registerUser("username", email, password);
      console.log("Регистрация успешна:", result);
      setVerifying(true);
    } catch (error) {
      console.error("Ошибка:", error);
      alert("Ошибка верификации. Проверьте код или данные.");
    }
  }

  return (
    <>
      <Link to="/">
        <img className={styles.closeBtn} src="/icons/close.png" alt="Close" />
      </Link>
      <div className={styles.registerContainer}>
        {verifying ? (
          <SuccessBunner />
        ) : (
          <>
            {success ? (
              <form className={styles.verifyingCard} onSubmit={verify}>
                <h1>Регистрация</h1>
                <p>Введите 8-и значный код, отправленный на вашу почту</p>
                <label htmlFor="code">Код</label>
                <input
                  type="text"
                  id="code"
                  name="code"
                  placeholder="Код"
                  // value={code}
                  // onChange={(e) => setCode(e.target.value)}
                />
                <button type="submit">Продолжить</button>
              </form>
            ) : (
              <>
                <LoginForm
                  title={"Регистрация"}
                  formType="register"
                  handleRegistre={registre}
                  login={email}
                  pass={password}
                  passRep={passwordRepeat}
                  handleEmail={setEmail}
                  handlePass={setPassword}
                  handlePassRep={setPasswordRepeat}
                />
                <div className={styles.loginText}>
                  Есть аккаунт? <Link to="/login">Войти</Link>
                </div>
              </>
            )}
          </>
        )}
      </div>
    </>
  );
};

export default Register;
