import React, { useState } from "react";
import styles from "../../../styles/GoalPopUp.module.css";
import PopUpContainer from "../Containers/PopUpContainer";
import CancelButton from "../Buttons/CancelButton";
import ProgressBar from "../ProgressBar/ProgressBar";
import CircleLogo from "../Circle/CircleLogo";
import AccentButton from "../Buttons/AccentButton";
import axios from "axios";
import TextArea from "../FormElems/TextArea";


const GoalPopUp = ({
    id,
    className,
    title,
    description,
    deadline,
    percentage,
    date,
    close,
    refresh
}) => {
    const [newPercentage, setNewPercentage] = useState(percentage);


    const handlePercentageChange = (newPercent) => {
        setNewPercentage(newPercent);
    };

    const editPercentage = async (newPercentage) => {
        console.log(id);
    
        try {
            const response = await axios.put(`${process.env.NEXT_PUBLIC_API_URL}/goals/${id}`, {
                id: id,
                name: title,
                description: description,
                deadline: deadline,
                state: newPercentage,
            });
            console.log(response);
        } catch (error) {
            console.log('Error updating percentage:', error);
        }
    
        refresh();
        close();
    };
    

    return (
        <PopUpContainer className={styles.GoalPopUp + " " + className}>
            <div className={styles.GoalPopUpTopBar}>
                <CircleLogo
                    image="/target.svg"
                    className={styles.GoalCircleLogo}
                />
                <div>
                    <p className={styles.GoalPopUpTitle}>{title}</p>
                    <p className={styles.GoalPopUpDate}>{date}</p>
                </div>
            </div>

             <p className={styles.GoalPopUpDescription}>{description}</p>
             <div className={styles.FlexRow}>
                <p className={styles.GoalPopUpDescription}>
                    Deadline: <span>{deadline}</span>
                </p>
                <p className={styles.GoalPopUpDescription}>
                    Progress: <span>{newPercentage}%</span>
                </p>
            </div>

            <ProgressBar
                percentage={newPercentage}
                className={styles.GoalProgressBar}
                onChangePercentage={handlePercentageChange}
                interactable = {true}
            />
            <div className={styles.FlexRowEnd}>
                {newPercentage != percentage && <AccentButton text="Save" onClick={() => editPercentage(newPercentage)}/>}
                <CancelButton text="Close" onClick={() => close()} />
            </div>
        </PopUpContainer>
    );
};
export default GoalPopUp;
