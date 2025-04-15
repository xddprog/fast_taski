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
        {item.labels.map((_, index) => (
          <>
            {item.title === "Команды" ? (
              <div className={styles.navbarLine}>
                <img src={item.icons[index]} alt="icon" />
                <p key={index}>Команда 1</p>
                <img src={"icons/arrow-downlight.png"} alt="icon" />
              </div>
            ) : (
              <></>
            )}
            <div className={styles.navbarLine}>
              <img src={item.icons[index]} alt="icon" />
              <p key={index}>{item.labels[index]}</p>
            </div>
          </>
        ))}
      </div>
    </div>
  );
};

export default NavbarGroup;
