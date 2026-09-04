import React, { useEffect, useState } from "react";
import styles from "../../../styles/ScoreCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import apiClient from "../../utils/apiClient";

const toNumber = (value) => {
    if (typeof value === "number") return value;
    const parsed = Number(value);
    return Number.isNaN(parsed) ? 0 : parsed;
};

const formatDate = (value) => {
    if (!value) return "";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString();
};

const ScoreCard = (props) => {
    const [Submissions, setSubmissions] = useState(undefined);
    const [TotalScore, setTotalScore] = useState(0);

    const getScoreData = async () => {
        if (!props.user_id) return;
        try {
            const submissionsResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/submissions/student/${props.user_id}`
            );
            const challengesResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges`
            );

            const challengeNames = {};
            (challengesResponse.data.challenges || []).forEach((challenge) => {
                challengeNames[challenge.id] = challenge.name;
            });

            const rawSubmissions = submissionsResponse.data.submissions || [];
            const enriched = rawSubmissions.map((submission) => ({
                ...submission,
                challengeName:
                    challengeNames[submission.challengeId] || submission.challengeId,
                score: toNumber(submission.score),
            }));

            setSubmissions(enriched);
            setTotalScore(toNumber(submissionsResponse.data.totalScore));
        } catch (err) {
            console.log(err);
            setSubmissions([]);
            setTotalScore(0);
        }
    };

    useEffect(() => {
        getScoreData();
    }, [props.user_id]);

    return (
        <DefaultContainer
            style={{ width: props.width }}
            className={styles.ScoreCard + " " + props.className}
            onClick={() => {}}
        >
            <p className={styles.Title}>Punctaj</p>
            <p className={styles.TotalScore}>Scor total: {TotalScore}</p>

            {Submissions === undefined ? (
                <p>Se încarcă...</p>
            ) : Submissions.length === 0 ? (
                <p>Niciun punctaj încă</p>
            ) : (
                <div className={styles.flexDiv}>
                    {Submissions.map((submission) => (
                        <div key={submission.id} className={styles.ScoreEntry}>
                            <div className={styles.ScoreEntryTop}>
                                <p className={styles.ChallengeName}>
                                    {submission.challengeName}
                                </p>
                                <p className={styles.ScoreValue}>{submission.score}</p>
                            </div>
                            <p className={styles.ScoreDate}>
                                {formatDate(submission.gradedDate)}
                            </p>
                            {submission.feedback ? (
                                <p className={styles.ScoreFeedback}>
                                    {submission.feedback}
                                </p>
                            ) : null}
                        </div>
                    ))}
                </div>
            )}
        </DefaultContainer>
    );
};

export default ScoreCard;
