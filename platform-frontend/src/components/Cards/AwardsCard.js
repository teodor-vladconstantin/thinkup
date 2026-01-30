import React, { useEffect } from "react";
import styles from "../../../styles/AwardsCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";

const AwardsCard = (props) => {
    useEffect(() => {
        //document.querySelector(".awardsContainer").style.width = props.width;
        var a1, a2, a3, a4;
        a1 = document.querySelector(".award1div");
        a2 = document.querySelector(".award2div");
        a3 = document.querySelector(".award3div");
        a4 = document.querySelector(".award4div");
        if (props.award1 == "true") a1.style.opacity = "1";
        else a1.style.opacity = "0";
        if (props.award2 == "true") a2.style.opacity = "1";
        else a2.style.opacity = "0";
        if (props.award3 == "true") a3.style.opacity = "1";
        else a3.style.opacity = "0";
        if (props.award4 == "true") a4.style.opacity = "1";
        else a4.style.opacity = "0";
    });
    return (
        <DefaultContainer
            style={{ width: props.width }}
            className={
                styles.AwardsCard +
                " " +
                props.className +
                " " +
                "awardsContainer"
            }
            onClick={() => {}}
        >
            <p className={styles.Title}>Awards</p>
            <div className={styles.AwardsGrid}>
                <div className={styles.Award + " " + "award1div"}>
                    <img src={props.src1} alt="award1" />
                    <p>{props.descr1}</p>
                </div>
                <div className={styles.Award + " " + "award2div"}>
                    <img src={props.src2} alt="award1" />
                    <p>{props.descr2}</p>
                </div>
                <div className={styles.Award + " " + "award3div"}>
                    <img src={props.src3} alt="award1" />
                    <p>{props.descr3}</p>
                </div>
                <div className={styles.Award + " " + "award4div"}>
                    <img src={props.src4} alt="award1" />
                    <p>{props.descr4}</p>
                </div>
            </div>
        </DefaultContainer>
    );
};
export default AwardsCard;
