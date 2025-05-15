import styles from "./NavbarGroup.module.scss";

interface NavbarGroupProps {
  item: {
    title?: string;
    icons: Array<string>;
    labels: Array<string>;
  };
}

const NavbarGroup: React.FC<NavbarGroupProps> = ({ item }) => {
  return (
    <div className={styles.navbarGroups}>
      {item.title !== undefined ? <h3>{item.title}</h3> : <></>}
      <div className={styles.navbarGroup}>
        {item.labels.map((label, index) => (
          <>
            {item.title === "Команды" ? (
              <div key={item.title} className={styles.navbarLine}>
                <img src={item.icons[index]} alt="icon" />
                <p>Команда 1</p>
                <img src={"icons/arrow-downlight.png"} alt="icon" />
              </div>
            ) : (
              <></>
            )}
            <div key={index} className={styles.navbarLine}>
              <img src={item.icons[index]} alt="icon" />
              <p>{label}</p>
            </div>
          </>
        ))}
      </div>
    </div>
  );
};

export default NavbarGroup;
