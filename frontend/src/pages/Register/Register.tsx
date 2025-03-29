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
    const formData = new FormData(event.currentTarget);
    const registerData: RegisterUserInterface = {
      username: formData.get("username") as string,
      email: formData.get("email") as string,
      password: formData.get("password") as string,
    };

    await authService.checkUserExist(registerData).then(res => {
      if (res.status === 200) {
        setUserForm(registerData);
        setSuccess(true);
      }
    });
  }

  async function verify()  {
    if (!codeRef.current || codeRef.current.value.length !== 6) {
      return alert("Введите корректный код");
    };
    await authService.registerUser(userForm as RegisterUserInterface, codeRef.current.value).then(res => {
      console.log(res);
    });
    setVerifying(true);
  }

  return (
    <>
      <Link to="/">
        <img className={styles.closeBtn} src="/icons/close.png" />
      </Link>
      <div className={styles.registerContainer}>
        {verifying ? (
          <SuccessBunner
            description={"Вы успешно зарегистрировались"}
          ></SuccessBunner>
        ) : (
          <>
            {success ? (
              <div className={styles.verifyingCard}>
                <h1>Регистрация</h1>
                <p>Введите 6-и значный код, отправленный на вашу почту</p>
                <label htmlFor="code">Код</label>
                <input type="text" id="code" name="code" placeholder="Код" ref={codeRef} />
                <button onClick={verify}>Продолжить</button>
              </div>
            ) : (
              <LoginForm
                title={"Регистрация"}
                formType="register"
                handleRegistre={registre}
              ></LoginForm>
            )}
          </>
        )}
      </div>
    </>
  );
};

export default Register;
