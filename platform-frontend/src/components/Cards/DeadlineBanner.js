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
            const projectsResponse = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/user_projects/${props.user_id}`
            );

            const challenges = challengesResponse.data.challenges || [];
            const projects = projectsResponse.data.projects || [];
            const participatingChallengeIds = new Set(
                projects.map((project) => project.challengeId)
            );

            const now = Date.now();

            const upcoming = challenges
                .filter(
                    (challenge) =>
                        !participatingChallengeIds.has(challenge.id)
                )
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
