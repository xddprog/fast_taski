import { Link } from "react-router-dom";
import styles from "./SuccessBunner.module.scss";

interface BunnerProps {
  description: string;
}

const SuccessBunner: React.FC<BunnerProps> = ({ description }) => {
  return (
    <div className={styles.successCard}>
      <h1>Успех!</h1>
      <p>{description}</p>
      <img src="/images/success_img.png" />
      <Link to="/">Продолжить</Link>
    </div>
  );
};

export default SuccessBunner;
