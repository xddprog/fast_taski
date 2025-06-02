import { useState, useEffect, ChangeEvent } from "react";
import styles from "./ProfileContainer.module.scss";
import imageCompression from "browser-image-compression";

export default function ProfileContainer() {
    const [fullName, setFullName] = useState("");
    const [publicName, setPublicName] = useState("");
    const [email, setEmail] = useState("");
    const [initialEmail, setInitialEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [avatarUrl, setAvatarUrl] = useState<string | null>(null);
    const [avatarFile, setAvatarFile] = useState<File | null>(null);
    const [_, setAvatarBase64] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [phoneError, setPhoneError] = useState<string | null>(null);

    useEffect(() => {
        if (error) {
            const timer = setTimeout(() => {
                setError(null);
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [error]);

    useEffect(() => {
        async function fetchUserData() {
            try {
                const response = await fetch(
                    "https://fasttaski.ru/api/v1/auth/current_user",
                    { credentials: "include" }
                );
                if (!response.ok)
                    throw new Error("Ошибка при получении пользователя");

                const data = await response.json();

                setFullName(data.username || "");
                setPublicName(data.public_name || data.username || "");
                setEmail(data.email || "");
                setInitialEmail(data.email || "");
                setPhone(data.phone_number || "");

                if (data.avatar && typeof data.avatar === "string") {
                    setAvatarUrl(
                        data.avatar.startsWith("http")
                            ? data.avatar
                            : `https://fasttaski.ru${data.avatar}`
                    );
                }
            } catch (err) {
                console.error("Ошибка загрузки профиля:", err);
            }
        }

        fetchUserData();
    }, []);

    function validatePhone(input: string): boolean {
        const phoneRegex = /^(\+7|8)\d{10}$/;
        return phoneRegex.test(input);
    }

    async function handleSave() {
        setLoading(true);
        setError(null);
    
        if (!validatePhone(phone)) {
            setError("Неверный формат номера телефона");
            setLoading(false);
            return;
        }
    
        try {
            const formData = new FormData();
    
            formData.append("username", fullName);
            formData.append("public_name", publicName);
            formData.append("phone_number", phone);
    
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
                // НЕ устанавливать Content-Type, браузер сделает это сам
            });
    
            if (!response.ok) {
                const errorData = await response.json();
                const message = errorData.detail || "Ошибка обновления профиля";
                setError(message);
                throw new Error(message);
            }
    
            const data = await response.json();
    
            if (data.avatar && typeof data.avatar === "string") {
                setAvatarUrl(
                    data.avatar.startsWith("http")
                        ? data.avatar
                        : `https://fasttaski.ru${data.avatar}`
                );
                setAvatarFile(null);
            }
    
            setPhone(data.phone_number || "");
            setEmail(data.email || "");
            setInitialEmail(data.email || "");
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

            // Конвертация в base64
            const base64 = await fileToBase64(compressed);
            setAvatarBase64(base64);
        } catch (err) {
            console.error("Ошибка при загрузке изображения", err);
            alert("Изображение слишком большое или сервер его не принял.");
        }
    }

    function fileToBase64(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                if (typeof reader.result === "string") resolve(reader.result);
                else reject("Ошибка чтения файла");
            };
            reader.onerror = (error) => reject(error);
        });
    }

    function handleAvatarRemove() {
        setAvatarUrl(null);
        setAvatarFile(null);
        setAvatarBase64(null);
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
                            {error && (
                                <p className={styles.errorMessage}>{error}</p>
                            )}
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
                                    Никнейм
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
                                        onChange={(e) => {
                                            const value = e.target.value;
                                            setPhone(value);

                                            if (
                                                value &&
                                                !validatePhone(value)
                                            ) {
                                                setPhoneError(
                                                    "Номер должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX"
                                                );
                                            } else {
                                                setPhoneError(null);
                                            }
                                        }}
                                        placeholder="+79991234567"
                                    />
                                    {phoneError && (
                                        <p className={styles.errorMessage}>
                                            {phoneError}
                                        </p>
                                    )}
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
