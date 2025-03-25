import styles from './Info.module.scss'

const Info:React.FC = () => {
  return (
    <section className={styles.infoContainer}>
        <div className={styles.fastTaskiInfo}>
            <img src="/icons/infoFastTaski.png" alt="infoFastTaski" />
            <h1>Эффективный помощник в <span className={styles.spanElement}>распределении задач</span></h1>
        </div>
        <img className={styles.image} src="/icons/infoImage.png" alt="infoImage" />
    </section>
  )
}

export default Info;