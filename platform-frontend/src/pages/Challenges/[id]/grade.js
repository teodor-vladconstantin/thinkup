import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import styles from "../../../../styles/GradeChallenge.module.css";
import apiClient from "../../../utils/apiClient";
import { useMyUserContext } from "../../../contexts/UserContext";
import ScrollContainer from "../../../components/Containers/ScrollContainer";

const GradeChallengePage = () => {
    const router = useRouter();
    const { id } = router.query;
    const user = useMyUserContext();
    const [Challenge, setChallenge] = useState(null);
    const [Projects, setProjects] = useState([]);
    const [Scores, setScores] = useState({});
    const [Feedbacks, setFeedbacks] = useState({});
    const [Status, setStatus] = useState({});

    const loadData = async () => {
        if (!id) return;
        try {
            const challengeResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges/${id}`
            );
            setChallenge(challengeResponse.data);

            const projectsResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/projects`
            );
            const allProjects = projectsResponse.data.projects || [];
            setProjects(allProjects.filter((p) => p.challengeId === id));
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {
        loadData();
    }, [id]);

    if (user === undefined) {
        return (
            <ScrollContainer>
                <p className={styles.NoAccess}>Se încarcă...</p>
            </ScrollContainer>
        );
    }

    if (user.role !== "Mentor") {
        return (
            <ScrollContainer>
                <p className={styles.NoAccess}>
                    Doar mentorii pot nota proiecte.
                </p>
            </ScrollContainer>
        );
    }

    const gradeProject = async (projectId) => {
        const score = Scores[projectId];
        if (score === undefined || score === "") {
            setStatus({ ...Status, [projectId]: "Introdu un scor." });
            return;
        }
        try {
            await apiClient.post(
                `${process.env.NEXT_PUBLIC_API_URL}/submissions/project/${projectId}`,
                {
                    score: Number(score),
                    feedback: Feedbacks[projectId] || "",
                }
            );
            setStatus({ ...Status, [projectId]: "Notat cu succes." });
        } catch (err) {
            console.log(err);
            setStatus({
                ...Status,
                [projectId]:
                    err.response?.data?.error || "A apărut o eroare la notare.",
            });
        }
    };

    return (
        <ScrollContainer className={styles.GradePage}>
            <h1>{Challenge ? Challenge.name : "Challenge"}</h1>
            <p>{Challenge ? Challenge.description : ""}</p>

            {Projects.length === 0 && (
                <p>Niciun proiect pe acest challenge încă.</p>
            )}

            {Projects.map((project) => (
                <div key={project.id} className={styles.ProjectRow}>
                    <h3>{project.name}</h3>
                    <p>{project.description}</p>
                    <div className={styles.GradeForm}>
                        <input
                            type="number"
                            placeholder="Scor"
                            value={Scores[project.id] || ""}
                            onChange={(e) =>
                                setScores({
                                    ...Scores,
                                    [project.id]: e.target.value,
                                })
                            }
                        />
                        <input
                            type="text"
                            placeholder="Feedback (opțional)"
                            value={Feedbacks[project.id] || ""}
                            onChange={(e) =>
                                setFeedbacks({
                                    ...Feedbacks,
                                    [project.id]: e.target.value,
                                })
                            }
                        />
                        <button onClick={() => gradeProject(project.id)}>
                            Notează
                        </button>
                    </div>
                    {Status[project.id] && <p>{Status[project.id]}</p>}
                </div>
            ))}
        </ScrollContainer>
    );
};

export default GradeChallengePage;
