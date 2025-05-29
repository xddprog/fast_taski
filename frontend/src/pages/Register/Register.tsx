import { Link } from "react-router-dom";
import styles from "./Register.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { FormEvent, useState } from "react";
import SuccessBunner from "../../components/SuccessBanner/SuccessBunner";
import { RegisterUserInterface } from "../../interfaces/authInterfaces";
import AuthService from "../../api/services/authService";

const Register: React.FC = () => {
  const [success, setSuccess] = useState(false);
  const [userForm, setUserForm] = useState<RegisterUserInterface | null>(null);

  const authService = new AuthService();

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
      const res = await authService.registerUser(registerData, "123");
      if (res.status === 201) {
        setSuccess(true);
      } else {
        alert("Произошла ошибка при регистрации. Попробуйте снова.");
      }
    } catch (error) {
      console.error("Ошибка регистрации:", error);
      alert("Вы уже зарегистрированы!");
    }
  }

  return (
    <>
      <Link to="/">
        <img className={styles.closeBtn} src="/icons/close.png" alt="Close" />
      </Link>
      <div className={styles.registerContainer}>
        {success ? (
          <SuccessBunner />
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
      </div>
    </>
  );
};

export default Register;
