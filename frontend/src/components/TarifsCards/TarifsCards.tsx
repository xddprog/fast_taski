import TarifCard from "../TarifCard/TarifCard";
import styles from "./TarifsCards.module.scss";

const tariffs = [
  {
    id: 1,
    title: "Базовый тариф",
    description: "Тариф с доступом к базовому функционалу сервиса",
    price: "Бесплатно",
    feature_description: "Базовый функционал сервиса и...",
    features: ["10 задач в день", "1 пользователь", "Базовая поддержка"],
  },
  {
    id: 2,
    title: "Безграничный тариф",
    description:
      "Тариф с полным доступом ко всем фишкам системы без ограничений и лимитов",
    price: "9999₽",
    feature_description: "Все фишки из базового и «Плюс» тарифов, и...",
    features: [
      "Неограниченные задачи",
      "До 5 пользователей",
      "Приоритетная поддержка",
      "Аналитика",
    ],
  },
  {
    id: 3,
    title: "Тариф «Плюс»",
    description: "Тариф с расширенным доступом к функционалу сервиса",
    price: "2999₽",
    feature_description: "Все фишки из базового тарифа и...",
    features: [
      "Неограниченные задачи",
      "Неограниченные пользователи",
      "Персональный менеджер",
      "Интеграции API",
      "Кастомные отчеты",
    ],
  },
];

const TarifsCards: React.FC = () => {
  const reorderedTariffs = [
    ...tariffs.filter((t) => t.id === 2),
    ...tariffs.filter((t) => t.id !== 1 && t.id !== 2),
    ...tariffs.filter((t) => t.id === 1),
  ];

  return (
    <>
      <section className={styles.tarifsCardsContainer}>
        {tariffs.map((tariff) => (
          <TarifCard
            key={tariff.id}
            id={tariff.id}
            title={tariff.title}
            price={tariff.price}
            description={tariff.description}
            feature_description={tariff.feature_description}
            features={tariff.features}
          />
        ))}
      </section>

      <section className={styles.tarifsCardsContainerMob}>
        {reorderedTariffs.map((tariff) => (
          <TarifCard
            key={tariff.id}
            id={tariff.id}
            title={tariff.title}
            price={tariff.price}
            description={tariff.description}
            feature_description={tariff.feature_description}
            features={tariff.features}
          />
        ))}
      </section>
    </>
  );
};

export default TarifsCards;
