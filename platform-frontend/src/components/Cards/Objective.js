import React, { useEffect } from "react";
import styles from "../../../styles/Objective.module.css";
import DefaultContainer from "../Containers/DefaultContainer";

const ObjectivesCard = (props) => {
    useEffect(() => {
        var img = document.querySelector("." + props.id);
        if (props.completed == "true") img.style.opacity = "1";
        else img.style.opacity = "0";
    });
    return (
        <DefaultContainer
            className={styles.Objective + " " + props.className}
            onClick={() => {}}
        >
            <p>{props.text}</p>
            <img src="/checked-icon.svg" alt="checked" className={props.id} />
        </DefaultContainer>
    );
};
export default ObjectivesCard;
