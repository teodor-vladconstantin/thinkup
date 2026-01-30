import React, { useEffect, useState } from "react";
import styles from "../../../styles/ObjectivesCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import Objective from "./Objective.js";
import NewObjectiveCard from "../Cards/NewObjectiveCard";
import { AnimatePresence } from "framer-motion";
import NewObjectivePopUp from "../PopUp/NewObjectivePopUp.js";
import CircleAddButton from "../Buttons/CircleAddButton";



const ObjectivesCard = (props) => {
    useEffect(() => {
        document.querySelector(".objectivesContainer").style.width =
            props.width;
    });

    const [NewObjectivePopUpState, setNewGoalPopUpState] = useState(false);

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
            {props.access == "true" ? (
                <div className={styles.flexDiv}>
                    <Objective
                        id="obj1"
                        text={props.objective1}
                        completed="true"
                    ></Objective>
                    <Objective
                        id="obj2"
                        text={props.objective2}
                        completed="true"
                    ></Objective>
                    <Objective
                        id="obj3"
                        text={props.objective3}
                        completed="false"
                    ></Objective>
                    <NewObjectiveCard 
                    onClick={() => setNewGoalPopUpState(true)}
                    />
                </div>
            ) : (
                <p>Objectives only visible to user and mentors.</p>
            )}
            <AnimatePresence exitBeforeEnter={true}>
                {
                    NewObjectivePopUpState && 
                    (
                        <NewObjectivePopUp close={() => setNewGoalPopUpState(false)} />
                    )
                }
            </AnimatePresence>
        </DefaultContainer>
    );
};
export default ObjectivesCard;
