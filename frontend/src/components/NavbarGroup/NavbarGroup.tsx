import React, { useEffect, useState } from "react";
import styles from "./NavbarGroup.module.scss";

interface Team {
  id: number;
  name: string;
}

const NavbarGroup: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);

  useEffect(() => {
    const getTeams = async (): Promise<void> => {
      try {
        const response = await fetch("https://fasttaski.ru/api/v1/user/teams", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Ошибка запроса: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        setTeams(data);
      } catch (error) {
        console.error("Ошибка при GET-запросе:", error);
      }
    };

    getTeams();
  }, []);

  return (
    <div className={styles.navbarGroups}>
      {teams.map((team) => (
        <div key={team.id} className={styles.navbarLine}>
          <p>{team.name}</p>
        </div>
      ))}
    </div>
  );
};

export default NavbarGroup;
