import React, { useState, useEffect } from "react";
import styles from "../../../styles/ProjectsTable.module.css";
import ProjectCard from "../Cards/ProjectCard";
import NewProjectCard from "../Cards/NewProjectCard";
import { motion } from "framer-motion";
import { useRouter } from "next/router";
import ScrollContainer from "../Containers/ScrollContainer";
import axios from "axios";

const ProjectsTable = (props) => {
    const router = useRouter();
    const [Challenges, setChallenges] = useState([]);

    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/challenges`
                );
                setChallenges(response.data.challenges || []);
            } catch (err) {
                console.log(err);
            }
        };
        fetchChallenges();
    }, []);

    if (props.data == undefined) return <></>;

    return (
        <div className={styles.ProjectsTableContainer}>
            <ScrollContainer
                className={styles.ProjectsTable + " " + props.className}
                onClick={() => {}}
            >
                {props.data.map((projectdata, index) => {
                    if (projectdata.addcard == true)
                        return (
                            <NewProjectCard
                                onClick={() => router.push("/NewProject")}
                                key={index}
                            />
                        );
                    const challengeIndex = Challenges.findIndex(
                        (c) => c.id === projectdata.challengeId
                    );
                    const challengeName =
                        challengeIndex >= 0
                            ? Challenges[challengeIndex].name
                            : "";
                    return (
                        <ProjectCard
                            title={projectdata.name}
                            animation_delay={index + 1}
                            key={index}
                            id={projectdata.id}
                            category={challengeName}
                            colorIndex={challengeIndex >= 0 ? challengeIndex : 0}
                            thumbnail={projectdata.thumbnail}
                            thumbnail_extension={projectdata.thumbnail_extension}
                        >
                            {projectdata.description}
                        </ProjectCard>
                    );
                })}
            </ScrollContainer>
            <div className={styles.ProjectsTableShadow}></div>
        </div>
    );
};

export default ProjectsTable;
