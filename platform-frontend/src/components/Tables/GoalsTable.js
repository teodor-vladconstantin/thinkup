import React, { Children, useState } from "react";
import styles from "../../../styles/GoalsTable.module.css";
import GoalCard from "../Cards/GoalCard";
import DefaultContainer from "../Containers/DefaultContainer";
import NewGoalCard from "../Cards/NewGoalCard";
import GoalPopUp from "../PopUp/GoalPopUp";
import NewGoalPopUp from "../PopUp/NewGoalPopUp";
import { AnimatePresence } from "framer-motion";

const GoalsTable = (props) => {
    const [OpenedGoal, setOpenedGoal] = useState(null);
    const [NewGoalPopUpState, setNewGoalPopUpState] = useState(false);
    

    if (props.data == null)
        return (
            <DefaultContainer
                className={styles.GoalsTableContainer + " " + props.className}
                onClick={() => {}}
            ></DefaultContainer>
        );

    return (
        <DefaultContainer
            className={styles.GoalsTableContainer + " " + props.className}
            onClick={() => {}}
        >
            <p className={styles.GoalsTableTitle}>Goals</p>
            {props.AdminState ? (
                <NewGoalCard onClick={() => setNewGoalPopUpState(true)} />
            ) : (
                <></>
            )}
            {props.data.map((data, index) => {
                return (
                    <GoalCard
                        deadline={data.deadline}
                        title={data.name}
                        percentage={data.state}
                        onClick={() => setOpenedGoal(index)}
                        key={index}
                    />
                );
            })}

            <AnimatePresence exitBeforeEnter={true}>
                {OpenedGoal != null && (
                    <GoalPopUp
                        id={props.data[OpenedGoal].id}
                        close={() => setOpenedGoal(null)}
                        deadline={props.data[OpenedGoal].deadline}
                        title={props.data[OpenedGoal].name}
                        description={props.data[OpenedGoal].description}
                        percentage={props.data[OpenedGoal].state}
                        interactable={true}
                        refresh={props.refresh}
                    />
                )}
                {NewGoalPopUpState && (
                    <NewGoalPopUp
                        close={() => setNewGoalPopUpState(false)}
                        addedgoal={() => {
                            setNewGoalPopUpState(false);
                            props.getProjectData();
                        }}
                        projectId={props.ProjectId}
                    />
                )}
            </AnimatePresence>
        </DefaultContainer>
    );
};
export default GoalsTable;
