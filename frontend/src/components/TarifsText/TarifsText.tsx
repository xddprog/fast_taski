import styles from "./TarifsText.module.scss";

const TarifsText: React.FC = () => {
  return (
    <section className={styles.tarifsText}>
      <div className={styles.tarifsTextContent}>
        <h1>Тарифные планы</h1>
        <p>
          У нас есть тарифы, которые <span>подойдут каждому!</span>
        </p>
      </div>
      <div className={styles.imgContainer}>
        <img src="/images/tarifs_img.png" />
      </div>
    </section>
  );
};

export default TarifsText;
