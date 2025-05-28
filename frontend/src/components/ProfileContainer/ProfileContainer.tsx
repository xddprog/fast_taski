import { useState } from "react";
import styles from "./ProfileContainer.module.scss";

export default function ProfileContainer() {
    const [fullName, setFullName] = useState("");
    const [publicName, setPublicName] = useState("");
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");

    return (
        <section className={styles.profileContainer}>
            <h1 className={styles.title}>Параметры профиля</h1>
            <div className={styles.containerForInfo}>
                <h2>Фото профиля</h2>
                <div className={styles.blockWithAvatar}>
                    <div className={styles.profilePhoto}>
                        <img
                            src="/images/Avatar.png"
                            alt="Фото профиля"
                            className={styles.photo}
                        />
                        <div className={styles.btns}>
                            <button className={styles.firstButton}>
                                <img src="/images/ImageUpload.png" alt="" />
                                Загрузить
                            </button>
                            <button className={styles.secondButton}>
                                <img src="/images/Trash.png" alt="" />
                                Удалить
                            </button>
                        </div>
                    </div>
                    <div className={styles.changesButton}>
                        <h1 className={styles.uSure}>Сохранить изменения?</h1>
                        <div className={styles.containerForBtns}>
                            <button className={styles.first}>Сохранить</button>
                            <button className={styles.second}>Отменить</button>
                        </div>
                    </div>
                </div>

                <div className={styles.personalData}>
                    <h2>Личные данные</h2>
                    <div className={styles.containerForInputs}>
                        <label>
                            Полное имя
                            <input
                                type="text"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                placeholder="Имя"
                            />
                        </label>
                        <label>
                            Публичное имя
                            <input
                                type="text"
                                value={publicName}
                                onChange={(e) => setPublicName(e.target.value)}
                                placeholder="Публичное имя"
                            />
                        </label>
                        <label>
                            Почта
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="mail@mail.mail"
                            />
                        </label>
                        <label>
                            Телефон
                            <input
                                type="text"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                                placeholder="+99999999999"
                            />
                        </label>
                    </div>

                    
                </div>
            </div>
        </section>
    );
}
