import React, { useState, useEffect } from "react";
import styles from "../../../styles/Challenges.module.css";
import apiClient from "../../utils/apiClient";
import { useMyUserContext } from "../../contexts/UserContext";
import ScrollContainer from "../../components/Containers/ScrollContainer";
import { useRouter } from "next/router";

const emptyForm = {
    id: "",
    name: "",
    description: "",
    deadline: "",
    maxScore: 100,
};

const ChallengesPage = () => {
    const user = useMyUserContext();
    const router = useRouter();
    const [Challenges, setChallenges] = useState([]);
    const [Form, setForm] = useState(emptyForm);
    const [EditingId, setEditingId] = useState(null);
    const [Error, setError] = useState("");

    const loadChallenges = async () => {
        try {
            const response = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges`
            );
            setChallenges(response.data.challenges || []);
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {
        loadChallenges();
    }, []);

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
                    Doar mentorii pot gestiona challenge-urile.
                </p>
            </ScrollContainer>
        );
    }

    const startEdit = (challenge) => {
        setEditingId(challenge.id);
        setForm({
            id: challenge.id,
            name: challenge.name,
            description: challenge.description,
            deadline: challenge.deadline,
            maxScore: challenge.maxScore,
        });
    };

    const resetForm = () => {
        setEditingId(null);
        setForm(emptyForm);
        setError("");
    };

    const submitForm = async () => {
        if (!Form.id || !Form.name || !Form.deadline) {
            setError("Id, nume și deadline sunt obligatorii.");
            return;
        }
        const duplicateName = Challenges.some(
            (c) => c.name === Form.name && c.id !== EditingId
        );
        if (duplicateName) {
            setError("Există deja un challenge cu acest nume.");
            return;
        }
        setError("");
        try {
            if (EditingId) {
                await apiClient.put(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges/${EditingId}`,
                    {
                        name: Form.name,
                        description: Form.description,
                        deadline: Form.deadline,
                        maxScore: Number(Form.maxScore),
                    }
                );
            } else {
                await apiClient.post(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges/${Form.id}`,
                    {
                        name: Form.name,
                        description: Form.description,
                        deadline: Form.deadline,
                        maxScore: Number(Form.maxScore),
                        created_by: user.id,
                        creation_date: new Date().toISOString(),
                    }
                );
            }
            resetForm();
            await loadChallenges();
        } catch (err) {
            console.log(err);
            setError(
                err.response?.data?.error || "A apărut o eroare la salvare."
            );
        }
    };

    const deleteChallenge = async (id) => {
        try {
            await apiClient.delete(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges/${id}`
            );
            await loadChallenges();
        } catch (err) {
            console.log(err);
            setError(
                err.response?.data?.error || "A apărut o eroare la ștergere."
            );
        }
    };

    return (
        <ScrollContainer className={styles.ChallengesPage}>
            <h1>Challenges</h1>

            <div className={styles.ChallengeForm}>
                <h3>{EditingId ? "Editează challenge" : "Challenge nou"}</h3>
                {!EditingId && (
                    <input
                        placeholder="id (ex: challenge-1)"
                        value={Form.id}
                        onChange={(e) =>
                            setForm({ ...Form, id: e.target.value })
                        }
                    />
                )}
                <input
                    placeholder="Nume (ex: Challenge 1)"
                    value={Form.name}
                    onChange={(e) => setForm({ ...Form, name: e.target.value })}
                />
                <textarea
                    placeholder="Descriere"
                    value={Form.description}
                    onChange={(e) =>
                        setForm({ ...Form, description: e.target.value })
                    }
                />
                <input
                    type="datetime-local"
                    value={Form.deadline}
                    onChange={(e) =>
                        setForm({ ...Form, deadline: e.target.value })
                    }
                />
                <input
                    type="number"
                    placeholder="Scor maxim"
                    value={Form.maxScore}
                    onChange={(e) =>
                        setForm({ ...Form, maxScore: e.target.value })
                    }
                />
                {Error && <p style={{ color: "red" }}>{Error}</p>}
                <div>
                    <button onClick={submitForm}>
                        {EditingId ? "Salvează" : "Creează"}
                    </button>
                    {EditingId && (
                        <button onClick={resetForm}>Anulează</button>
                    )}
                </div>
            </div>

            {Challenges.map((challenge) => (
                <div key={challenge.id} className={styles.ChallengeRow}>
                    <div>
                        <h3>{challenge.name}</h3>
                        <p>{challenge.description}</p>
                        <p>
                            Deadline: {challenge.deadline} · Scor max:{" "}
                            {challenge.maxScore}
                        </p>
                    </div>
                    <div className={styles.ChallengeActions}>
                        <button onClick={() => router.push(`/Challenges/${challenge.id}/grade`)}>
                            Notează
                        </button>
                        <button onClick={() => startEdit(challenge)}>
                            Editează
                        </button>
                        <button onClick={() => deleteChallenge(challenge.id)}>
                            Șterge
                        </button>
                    </div>
                </div>
            ))}
        </ScrollContainer>
    );
};

export default ChallengesPage;
