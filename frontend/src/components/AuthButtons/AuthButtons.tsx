import styles from "./AuthButtons.module.scss";

interface AuthParams {
  yandexAuth: (event: React.MouseEvent<HTMLButtonElement>) => void;
  vkauth: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const AuthButtons: React.FC<AuthParams> = ({ yandexAuth, vkauth }) => {
  return (  
    <div className={styles.otherVariant}>
      <h3>или продолжить с помощью</h3>
      <div className={styles.buttonContainer}>
        <button className={styles.yandexID} onClick={yandexAuth}>
          Яндекс ID
        </button>
        <button className={styles.vkID} onClick={vkauth}>
          VK ID
        </button>
      </div>
    </div>
  );
};

export default AuthButtons;
