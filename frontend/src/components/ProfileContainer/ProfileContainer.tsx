import { useState, useEffect } from "react";
import styles from "./ProfileContainer.module.scss";

export default function ProfileContainer() {
    const [fullName, setFullName] = useState("");
    const [publicName, setPublicName] = useState("");
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        async function fetchUserData() {
            try {
                const response = await fetch('https://fasttaski.ru/api/v1/auth/current_user', {
                    credentials: 'include',
                });
                if (!response.ok) throw new Error("Ошибка при получении пользователя");
                const data = await response.json();

                setFullName(data.username || "");
                setPublicName(data.public_name || data.username || "");
                setEmail(data.email || "");
                if (data.phone) setPhone(data.phone);
            } catch (err) {
                console.error("Ошибка загрузки профиля:", err);
                setError("Не удалось загрузить данные.");
            }
        }

        fetchUserData();
    }, []);

    async function handleSave() {
        setLoading(true);
        setError("");
        setSuccess(false);

        try {
            const response = await fetch("https://fasttaski.ru/api/v1/user/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify({
                    username: fullName,
                    public_name: publicName,
                    email: email,
                    phone: phone,
                }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || "Ошибка обновления профиля");
            }

            setSuccess(true);
        } catch (err) {
            console.error(err);
            setError("Не удалось сохранить изменения.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <section className={styles.profileContainer}>
            <h1 className={styles.title}>Параметры профиля</h1>
            <div className={styles.containerForInfo}>
                <h2>Фото профиля</h2>
                <div className={styles.rowWith}>
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
                    <div className={styles.changesButton}>
                        <h1 className={styles.uSure}>Сохранить изменения?</h1>
                        <div className={styles.containerForBtns}>
                            <button
                                className={styles.first}
                                onClick={handleSave}
                                disabled={loading}
                            >
                                {loading ? "Сохраняем..." : "Сохранить"}
                            </button>
                            <button
                                className={styles.second}
                                onClick={() => window.location.reload()}
                            >
                                Отменить
                            </button>
                        </div>
                        {error && <p className={styles.error}>{error}</p>}
                        {success && <p className={styles.success}>Изменения сохранены!</p>}
                    </div>
                </div>
            </div>
        </section>
    );
}
