import { Link } from "react-router-dom";
import styles from "./SuccessBunner.module.scss";

const SuccessBunner: React.FC = () => {
  return (
    <div className={styles.successCard}>
      <h1>Успех!</h1>
      <p>Операция прошла успешно</p>
      <img src="/images/success_img.png" />
      <Link to="/dashboard">Продолжить</Link>
    </div>
  );
};

export default SuccessBunner;
