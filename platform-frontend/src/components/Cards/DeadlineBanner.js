import React, { useEffect, useState } from "react";
import styles from "../../../styles/DeadlineBanner.module.css";
import apiClient from "../../utils/apiClient";

const HOURS_48_MS = 48 * 60 * 60 * 1000;

const formatRemaining = (ms) => {
    const totalHours = Math.floor(ms / (60 * 60 * 1000));
    const days = Math.floor(totalHours / 24);
    const hours = totalHours % 24;

    if (days > 0) {
        const dayLabel = days === 1 ? "zi" : "zile";
        return `${days} ${dayLabel} ${hours}h rămase`;
    }
    return `${hours}h rămase`;
};

const DeadlineBanner = (props) => {
    const [Banners, setBanners] = useState([]);

    const getDeadlineData = async () => {
        if (!props.user_id) {
            setBanners([]);
            return;
        }
        try {
            const challengesResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/challenges`
            );
            const submissionsResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/submissions/student/${props.user_id}`
            );

            const challenges = challengesResponse.data.challenges || [];
            const submissions = submissionsResponse.data.submissions || [];
            const submittedChallengeIds = new Set(
                submissions.map((submission) => submission.challengeId)
            );

            const now = Date.now();

            const upcoming = challenges
                .filter((challenge) => !submittedChallengeIds.has(challenge.id))
                .map((challenge) => ({
                    ...challenge,
                    msRemaining: new Date(challenge.deadline).getTime() - now,
                }))
                .filter(
                    (challenge) =>
                        !Number.isNaN(challenge.msRemaining) &&
                        challenge.msRemaining > 0 &&
                        challenge.msRemaining < HOURS_48_MS
                );

            setBanners(upcoming);
        } catch (err) {
            console.log(err);
            setBanners([]);
        }
    };

    useEffect(() => {
        getDeadlineData();
    }, [props.user_id]);

    if (Banners.length === 0) return null;

    return (
        <div className={styles.DeadlineBannerList}>
            {Banners.map((banner) => (
                <div key={banner.id} className={styles.DeadlineBanner}>
                    <span className={styles.BannerText}>
                        {banner.name} — {formatRemaining(banner.msRemaining)}
                    </span>
                </div>
            ))}
        </div>
    );
};

export default DeadlineBanner;
