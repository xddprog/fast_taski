import { useState } from "react";
import styles from "./ProfileContainer.module.scss";

export default function ProfileContainer() {
    const [fullName, setFullName] = useState("");
    const [publicName, setPublicName] = useState("");
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [position, setPosition] = useState("");
    const [department, setDepartment] = useState("");
    const [organization, setOrganization] = useState("");
    const [location, setLocation] = useState("");

    return (
        <section className={styles.profileContainer}>
            <h1 className={styles.title}>Профиль</h1>
            <div className={styles.containerForInfo}>
                <div className={styles.profilePhoto}>
                    <h2>Фото профиля</h2>
                    <img
                        src="/icons/Avatar.png"
                        alt="Фото профиля"
                        className={styles.photo}
                    />
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

                <div className={styles.personalData}>
                    <h2>Дополнительная информация</h2>
                    <div className={styles.containerForInputs}>
                        <label>
                            Должность
                            <input
                                type="text"
                                value={position}
                                onChange={(e) => setPosition(e.target.value)}
                                placeholder="Должность"
                            />
                        </label>
                        <label>
                            Отдел
                            <input
                                type="text"
                                value={department}
                                onChange={(e) => setDepartment(e.target.value)}
                                placeholder="Отдел"
                            />
                        </label>
                        <label>
                            Организация
                            <input
                                type="text"
                                value={organization}
                                onChange={(e) =>
                                    setOrganization(e.target.value)
                                }
                                placeholder="Организация"
                            />
                        </label>
                        <label>
                            Расположение
                            <input
                                type="text"
                                value={location}
                                onChange={(e) =>
                                    setLocation(e.target.value)
                                }
                                placeholder="Расположение"
                            />
                        </label>
                    </div>
                </div>
            </div>
        </section>
    );
}
