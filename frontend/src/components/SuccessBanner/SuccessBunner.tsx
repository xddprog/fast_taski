import { Link } from "react-router-dom";
import styles from "./SuccessBunner.module.scss";

const SuccessBunner: React.FC = () => {
  return (
    <div className={styles.successCard}>
      <h1>Успех!</h1>
      <p>Вы успешно зарегистрировались</p>
      <img src="/images/success_img.png" />
      <Link to="/">Продолжить</Link>
    </div>
  );
};

export default SuccessBunner;
