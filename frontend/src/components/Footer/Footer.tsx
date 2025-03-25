import styles from "./Footer.module.scss";

const Footer: React.FC = () => {
  return (
    <footer>
      <div className={styles.logoAndText}>
        <img src="/icons/infoFastTaski.png" />
        <p>Copyright © 2025 Fast TASK</p>
      </div>
      <div className={styles.icons}>
        <p>Наши социальные сети</p>
        <div className={styles.socialMediaRow}>
          <img src="icons/tg_white.png" />
          <img src="icons/vk_white.png" />
          <img src="icons/reddit_white.png" />
        </div>
      </div>
    </footer>
  );
};

export default Footer;
