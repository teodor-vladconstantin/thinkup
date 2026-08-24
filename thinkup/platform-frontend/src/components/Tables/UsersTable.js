import React, { useState } from "react";
import styles from "../../../styles/UsersTable.module.css";
import ProjectCard from "../Cards/ProjectCard";
import NewProjectCard from "../Cards/NewProjectCard";
import { motion } from "framer-motion";
import { useRouter } from "next/router";
import ScrollContainer from "../Containers/ScrollContainer";
import UserCard from "../Cards/UserCard";

const UsersTable = (props) => {
    /*<div className={styles.ProjectsTableShadow}></div>*/

    const router = useRouter();

    if (props.data == undefined) return <></>;

    return (
        <div className={styles.UsersTableContainer}>
            <ScrollContainer
                className={styles.UsersTable + " " + props.className}
                onClick={() => {}}
            >
                {props.data.map((userdata, index) => {
                    return (
                        <UserCard name={userdata.name} key={index} profile_picture={userdata.profile_picture} profile_picture_extension={userdata.profile_picture_extension} onClick={()=>router.push(`/Profile/${userdata.id}`)}></UserCard>
                    );
                })}
            </ScrollContainer>
        </div>
    );
};

export default UsersTable;
