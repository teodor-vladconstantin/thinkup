import React from "react";
import styles from "../../../styles/FeedbackPopUp.module.css";
import CancelButton from "../Buttons/CancelButton";
import PopUpContainer from "../Containers/PopUpContainer";
import CircleLogo from "../Circle/CircleLogo";

const FeedbackPopUp = ({ className, text, date, close, mentor_id}) => {
    return (
        <PopUpContainer className={styles.FeedbackPopUp + " " + className}>

            <p className={styles.FeedbackPopUpText}>{text}</p>

            <div className={styles.FeedbackButtonDiv}>
                <CancelButton text="Close" onClick={() => close()} />
            </div>

        </PopUpContainer>
    );
};
export default FeedbackPopUp;
