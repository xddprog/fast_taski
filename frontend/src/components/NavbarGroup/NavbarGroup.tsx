import React, { useEffect, useState } from "react";
import styles from "./NavbarGroup.module.scss";

interface Team {
  id: number;
  name: string;
  avatar: string;
}

const NavbarGroup: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [teamsForm, setTeamsForm] = useState(false);

  async function createTeam() {
    const Teamdata = {
      name: "Команда",
      description: "Описание",
      members: [],
    };

    const response = await fetch("https://fasttaski.ru/api/v1/team/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(Teamdata),
    });

    if (!response.ok) {
      const errorText = await response.text();
      alert("Команда с таким названием уже существует");
      throw new Error(`Ошибка запроса: ${response.status} - ${errorText}`);
    }

    const newData = await response.json();
    setTeams(newData);
  }

  async function createColumn() {
    const ColumnData = {
      name: "Новые задачи",
      color: "red",
    };

    const columnResponse = await fetch(
      `https://fasttaski.ru/api/v1/column/?team_id=${localStorage.getItem(
        "currentTeamsId"
      )}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(ColumnData),
      }
    );

    const columnData = await columnResponse.json();
    console.log(columnData);
  }

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
        if (data.length === 0) {
          createTeam();
          createColumn();
        } else {
          setTeams(data);
          localStorage.setItem("currentTeamId", data[0].id);
        }
      } catch (error) {
        console.error("Ошибка при GET-запросе:", error);
      }
    };

    getTeams();
  }, []);
  console.log(teams);

  function handleFormClick() {
    setTeamsForm(!teamsForm);
  }

  return (
    <>
      {teamsForm ? (
        <div className={styles.teamsContainer}>
          {teams.length > 1 &&
            teams.slice(1).map((team) => (
              <div key={team.id} className={styles.navbarLine}>
                {team.avatar === null ? (
                  <img src="images/Default.svg" alt="Default avatar" />
                ) : (
                  <img src={team.avatar} alt="Team avatar" />
                )}
                <p>{team.name}</p>
              </div>
            ))}
          <div className={styles.addTeamBtn} onClick={() => createTeam()}>
            <img src="icons/plus.svg" />
            <span>Новая команда</span>
          </div>
        </div>
      ) : (
        <></>
      )}

      <div className={styles.navbarGroups}>
        {teams.length > 1 && (
          <div key={teams[0].id} className={styles.navbarLine}>
            {teams[0].avatar === null ? (
              <img src="images/Default.svg" alt="Default avatar" />
            ) : (
              <img src={teams[0].avatar} alt="Team avatar" />
            )}
            <p>{teams[0].name}</p>
            <img
              src="icons/Arrow.svg"
              alt="Arrow icon"
              onClick={() => handleFormClick()}
            />
          </div>
        )}
      </div>
    </>
  );
};

export default NavbarGroup;
