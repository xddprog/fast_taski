import styles from "./TarifCard.module.scss";

interface TarifCardProps {
  id: number;
  title: string;
  price: string;
  description: string;
  feature_description: string;
  features: string[];
}

const TarifCard: React.FC<TarifCardProps> = ({
  id,
  title,
  price,
  description,
  feature_description,
  features,
}) => {
  const cardClass = id === 2 ? styles.tarifSpecialCard : styles.tarifCard;
  return (
    <div className={cardClass}>
      <h1 className={styles.tarifTitle}>{title}</h1>
      <p className={styles.description}>{description}</p>
      {id === 1 ? (
        <p className={styles.price}>{price}</p>
      ) : (
        <p className={styles.price}>
          {price} <span>в мес.</span>
        </p>
      )}
      <button className={styles.tarifBtn}>Подключить тариф</button>
      <p className={styles.featuresTitle}>Фишки:</p>
      <p className={styles.featuresDescription}>{feature_description}</p>
      <ul className={styles.featuresList}>
        {features.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </ul>
    </div>
  );
};

export default TarifCard;
