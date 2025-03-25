import { Link } from "react-router-dom";
import styles from "./Register.module.scss";
import LoginForm from "../../components/LoginForm/LoginForm";
import { useState } from "react";
import SuccessBunner from "../../components/SuccessBanner/SuccessBunner";

const Register: React.FC = () => {
  const [success, setSuccess] = useState(false);
  const [verifying, setVerifying] = useState(false);

  function registre() {
    setSuccess(true);
  }

  function verify() {
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
                <p>Введите 8-и значный код, отправленный на вашу почту</p>
                <label htmlFor="code">Код</label>
                <input type="text" id="code" name="code" placeholder="Код" />
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
