import React, { useState } from "react";
import styles from "../../../styles/ProjectsTable.module.css";
import ProjectCard from "../Cards/ProjectCard";
import NewProjectCard from "../Cards/NewProjectCard";
import { motion } from "framer-motion";
import { useRouter } from "next/router";
import ScrollContainer from "../Containers/ScrollContainer";

const ProjectsTable = (props) => {
    /*<div className={styles.ProjectsTableShadow}></div>*/

    const router = useRouter();

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
                    return (
                        <ProjectCard
                            title={projectdata.name}
                            animation_delay={index + 1}
                            key={index}
                            id={projectdata.id}
                            category={projectdata.areaOfImplementation}
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
