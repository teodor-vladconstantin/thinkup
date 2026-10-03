import React, { useEffect, useState } from "react";
import styles from "../../../styles/ObjectivesCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import Objective from "./Objective.js";
import NewObjectiveCard from "../Cards/NewObjectiveCard";
import { AnimatePresence } from "framer-motion";
import NewObjectivePopUp from "../PopUp/NewObjectivePopUp.js";
import apiClient from "../../utils/apiClient";

const ObjectivesCard = (props) => {
    useEffect(() => {
        document.querySelector(".objectivesContainer").style.width =
            props.width;
    });

    const [NewObjectivePopUpState, setNewGoalPopUpState] = useState(false);
    const [Objectives, setObjectives] = useState([]);

    const getObjectives = async () => {
        if (props.userId == undefined) return;
        try {
            const response = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/personal_objectives/user/${props.userId}`
            );
            setObjectives(response.data.objectives || []);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        if (props.access) getObjectives();
    }, [props.userId, props.access]);

    const toggleObjective = async (objective) => {
        const statePercentage = objective.state == 100 ? 0 : 100;
        try {
            await apiClient.put(
                `${process.env.NEXT_PUBLIC_API_URL}/personal_objectives/${objective.id}`,
                { statePercentage: statePercentage }
            );
            setObjectives((prev) =>
                prev.map((o) =>
                    o.id == objective.id ? { ...o, state: statePercentage } : o
                )
            );
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <DefaultContainer
            className={
                styles.ObjectivesCard +
                " " +
                props.className +
                " " +
                "objectivesContainer"
            }
            onClick={() => {}}
        >
            <p className={styles.Title}>Objectives</p>
            {props.access ? (
                <div className={styles.flexDiv}>
                    {Objectives.map((objective) => (
                        <Objective
                            key={objective.id}
                            text={objective.name}
                            completed={objective.state == 100}
                            onClick={
                                props.canEdit
                                    ? () => toggleObjective(objective)
                                    : undefined
                            }
                        ></Objective>
                    ))}
                    {Objectives.length == 0 && (
                        <p className={styles.Empty}>No objectives yet.</p>
                    )}
                    {props.canEdit && (
                        <NewObjectiveCard
                            onClick={() => setNewGoalPopUpState(true)}
                        />
                    )}
                </div>
            ) : (
                <p>Objectives only visible to user and mentors.</p>
            )}
            <AnimatePresence mode="wait">
                {
                    NewObjectivePopUpState &&
                    (
                        <NewObjectivePopUp
                            close={() => setNewGoalPopUpState(false)}
                            added={() => {
                                setNewGoalPopUpState(false);
                                getObjectives();
                            }}
                        />
                    )
                }
            </AnimatePresence>
        </DefaultContainer>
    );
};
export default ObjectivesCard;
