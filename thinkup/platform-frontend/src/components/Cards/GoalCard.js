import React, { Children } from "react";
import styles from "../../../styles/GoalCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import DefaultContainer2 from "../Containers/DefaultContainer2";
import ProgressBar from "../ProgressBar/ProgressBar";

const GoalCard = (props) =>{

    return (
        <DefaultContainer2 className={styles.GoalCard +" "+props.className} onClick={()=>props.onClick()}>
            <div className={styles.GoalCardContainer}>    
                <p className={styles.GoalCardDate}>{props.deadline}</p>
                <p className={styles.GoalCardTitle}>{props.title}</p>
            </div>
            <div className={styles.GoalCardContainer}>    
                <ProgressBar percentage={props.percentage} interactable={false}/>
                <p className={styles.GoalCardPercentage}>{props.percentage}%</p>
            </div>

        </DefaultContainer2>
    )
}
export default GoalCard;