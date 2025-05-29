import { useState, useEffect, ChangeEvent } from "react";
import styles from "./ProfileContainer.module.scss";
import imageCompression from "browser-image-compression";

export default function ProfileContainer() {
    const [fullName, setFullName] = useState("");
    const [publicName, setPublicName] = useState("");
    const [email, setEmail] = useState("");
    const [initialEmail, setInitialEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [_, setAvatarUrl] = useState<string | null>(null);
    const [avatarFile, setAvatarFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        async function fetchUserData() {
            try {
                const response = await fetch(
                    "https://fasttaski.ru/api/v1/auth/current_user",
                    {
                        credentials: "include",
                    }
                );
                if (!response.ok)
                    throw new Error("Ошибка при получении пользователя");
                const data = await response.json();

                setFullName(data.username || "");
                setPublicName(data.public_name || data.username || "");
                setEmail(data.email || "");
                setInitialEmail(data.email || "");
                if (data.phone) setPhone(data.phone);

                if (data.avatar && typeof data.avatar === "string") {
                    if (data.avatar.startsWith("http")) {
                        setAvatarUrl(data.avatar);
                    } else {
                        setAvatarUrl(`https://fasttaski.ru${data.avatar}`);
                    }
                }
            } catch (err) {
                console.error("Ошибка загрузки профиля:", err);
            }
        }

        fetchUserData();
    }, []);

    async function handleSave() {
        setLoading(true);

        try {
            const formData = new FormData();
            formData.append("username", fullName);
            formData.append("public_name", publicName);
            formData.append("phone", phone);
            if (email !== initialEmail) {
                formData.append("email", email);
            }
            if (avatarFile) {
                formData.append("avatar", avatarFile);
            }

            const response = await fetch("https://fasttaski.ru/api/v1/user/", {
                method: "PUT",
                credentials: "include",
                body: formData,
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

                throw new Error(
                    errorData.detail || "Ошибка обновления профиля"
                );
            }

            const data = await response.json();
            if (data.avatar && typeof data.avatar === "string") {
                if (data.avatar.startsWith("http")) {
                    setAvatarUrl(data.avatar);
                } else {
                    setAvatarUrl(`https://fasttaski.ru${data.avatar}`);
                }
                setAvatarFile(null);
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

        try {
            const compressed = await imageCompression(file, {
                maxSizeMB: 1,
                maxWidthOrHeight: 512,
                useWebWorker: true,
            });

            setAvatarFile(compressed);
            setAvatarUrl(URL.createObjectURL(compressed));
        } catch (err) {
            console.error("Ошибка при загрузке изображения", err);
            alert("Изображение слишком большое или сервер его не принял.");
        }
    }

    function handleAvatarRemove() {
        setAvatarUrl(null);
        setAvatarFile(null);
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
                                // src={avatarUrl || "/images/avatarImage.png"}
                                src={"/images/avatarImage.png"}
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
                                <button
                                    className={styles.secondButton}
                                    onClick={handleAvatarRemove}
                                >
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
                                        onChange={(e) =>
                                            setFullName(e.target.value)
                                        }
                                        placeholder="Имя"
                                    />
                                </label>
                                <label>
                                    Публичное имя
                                    <input
                                        type="text"
                                        value={publicName}
                                        onChange={(e) =>
                                            setPublicName(e.target.value)
                                        }
                                        placeholder="Публичное имя"
                                    />
                                </label>
                                <label>
                                    Почта
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) =>
                                            setEmail(e.target.value)
                                        }
                                        placeholder="mail@mail.mail"
                                    />
                                </label>
                                <label>
                                    Телефон
                                    <input
                                        type="text"
                                        value={phone}
                                        onChange={(e) =>
                                            setPhone(e.target.value)
                                        }
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
