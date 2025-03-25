import styles from './AufButtons.module.scss'

const AufButtons:React.FC = () => {
  return (
    <div className={styles.otherVariant}>
    <h3>или продолжить с помощью</h3>
    <div className={styles.buttonContainer}>
      <button className={styles.yandexID}>Яндекс ID</button>
      <button className={styles.vkID}>VK ID</button>
    </div>
  </div>
  )
}

export default AufButtons