import { Link } from "react-router-dom";
import styles from "./Register.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { FormEvent, useRef, useState } from "react";
import SuccessBunner from "../../components/SuccessBanner/SuccessBunner";
import { RegisterUserInterface } from "../../interfaces/authInterfaces";
import AuthService from "../../api/services/authService";

const Register: React.FC = () => {
  const [success, setSuccess] = useState(false);
  const [verifying, setVerifying] = useState(false);

  const authService = new AuthService();
  const [userForm, setUserForm] = useState<RegisterUserInterface | null>(null);
  const codeRef = useRef<HTMLInputElement>(null);

  async function registre(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const registerData: RegisterUserInterface = {
      username: formData.get("username") as string,
      email: formData.get("email") as string,
      password: formData.get("password") as string,
    };

    const passwordRepeat = formData.get("password_repeat") as string;
    if (registerData.password !== passwordRepeat) {
      alert("Пароли не совпадают");
      return;
    }

    try {
      const res = await authService.checkUserExist(registerData);
      if (res.status === 409) {
        alert("Пользователь с таким email или именем уже существует");
        return;
      }

      setUserForm(registerData);
      setSuccess(true);
    } catch (error) {
      console.error("Ошибка при проверке пользователя:", error);
      alert("Ошибка при проверке. Попробуйте позже.");
    }
  }

  async function verify(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!codeRef.current || codeRef.current.value.length !== 6) {
      alert("Введите корректный 6-значный код");
      return;
    }

    try {
      const res = await authService.registerUser(
        userForm as RegisterUserInterface,
        codeRef.current.value
      );
      console.log("Регистрация успешна:", res);
      setVerifying(true);
    } catch (error) {
      console.error("Ошибка верификации:", error);
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
                <p>Введите 6-и значный код, отправленный на вашу почту</p>
                <label htmlFor="code">Код</label>
                <input
                  type="text"
                  id="code"
                  name="code"
                  placeholder="Код"
                  ref={codeRef}
                />
                <button type="submit">Продолжить</button>
              </form>
            ) : (
              <>
                <LoginForm
                  title={"Регистрация"}
                  formType="register"
                  handleRegistre={registre}
                  login={userForm?.email || ""}
                  pass={userForm?.password || ""}
                  passRep={userForm?.password_repeat || ""}
                  handleEmail={(value) =>
                    setUserForm((prev) => ({ ...prev!, email: value }))
                  }
                  handlePass={(value) =>
                    setUserForm((prev) => ({ ...prev!, password: value }))
                  }
                  handlePassRep={(value) =>
                    setUserForm((prev) => ({
                      ...prev!,
                      password_repeat: value,
                    }))
                  }
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
