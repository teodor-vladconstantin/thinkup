import React from "react";
import styles from "../../../styles/Objective.module.css";
import DefaultContainer from "../Containers/DefaultContainer";

const Objective = (props) => {
    return (
        <DefaultContainer
            className={styles.Objective + " " + (props.onClick ? styles.Clickable : "") + " " + (props.className || "")}
            onClick={props.onClick}
        >
            <p>{props.text}</p>
            <img
                src="/checked-icon.svg"
                alt={props.completed ? "completed" : "not completed"}
                style={{ opacity: props.completed ? 1 : 0 }}
            />
        </DefaultContainer>
    );
};
export default Objective;
