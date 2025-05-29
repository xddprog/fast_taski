import { useState, useEffect, ChangeEvent } from "react";
import styles from "./ProfileContainer.module.scss";

export default function ProfileContainer() {
    const [fullName, setFullName] = useState("");
    const [publicName, setPublicName] = useState("");
    const [email, setEmail] = useState("");
    const [initialEmail, setInitialEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [avatarUrl, setAvatarUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        async function fetchUserData() {
            try {
                const response = await fetch("https://fasttaski.ru/api/v1/auth/current_user", {
                    credentials: "include",
                });
                if (!response.ok) throw new Error("Ошибка при получении пользователя");
                const data = await response.json();

                setFullName(data.username || "");
                setPublicName(data.public_name || data.username || "");
                setEmail(data.email || "");
                setInitialEmail(data.email || "");
                if (data.phone) setPhone(data.phone);
                if (data.avatar) setAvatarUrl(`https://fasttaski.ru${data.avatar}`);
            } catch (err) {
                console.error("Ошибка загрузки профиля:", err);
            }
        }

        fetchUserData();
    }, []);

    interface UserUpdatePayload {
        username: string;
        public_name: string;
        phone: string;
        email?: string;
        avatar?: string;
    }

    async function handleSave() {
        setLoading(true);

        const payload: UserUpdatePayload = {
            username: fullName,
            public_name: publicName,
            phone,
        };

        if (email !== initialEmail) {
            payload.email = email;
        }

        if (avatarUrl) {
            payload.avatar = avatarUrl.replace("https://fasttaski.ru", "");
        }

        try {
            const response = await fetch("https://fasttaski.ru/api/v1/user/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();

                if (
                    errorData?.detail &&
                    typeof errorData.detail === "string" &&
                    errorData.detail.includes("почтой")
                ) {
                    alert("Пользователь с таким e-mail уже существует.");
                    throw new Error("Email занят");
                }

                throw new Error(errorData.detail || "Ошибка обновления профиля");
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

    async function handleAvatarUpload(event: ChangeEvent<HTMLInputElement>) {
        const file = event.target.files?.[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("avatar", file);

        try {
            const response = await fetch("https://fasttaski.ru/api/v1/user/", {
                method: "POST",
                credentials: "include",
                body: formData,
            });

            if (!response.ok) throw new Error("Ошибка загрузки аватара");

            const data = await response.json();
            setAvatarUrl(`https://fasttaski.ru${data.path}`);
        } catch (err) {
            console.error(err);
            alert("Не удалось загрузить аватар");
        }
    }

    function handleAvatarRemove() {
        setAvatarUrl(null);
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
                                src={avatarUrl || "/images/avatarImage.png"}
                                alt="Фото профиля"
                                className={styles.photo}
                            />
                            <div className={styles.btns}>
                                <label className={styles.firstButton}>
                                    <img src="/images/ImageUpload.png" alt="" />
                                    Загрузить
                                    <input
                                        type="file"
                                        accept="image/*"
                                        onChange={handleAvatarUpload}
                                        hidden
                                    />
                                </label>
                                <button className={styles.secondButton} onClick={handleAvatarRemove}>
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
                    </div>
                </div>
            </div>
        </section>
    );
}
