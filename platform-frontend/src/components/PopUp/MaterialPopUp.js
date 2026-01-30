import React from "react";
import styles from "../../../styles/MaterialPopUp.module.css";
import CancelButton from "../Buttons/CancelButton";
import PopUpContainer from "../Containers/PopUpContainer";
import CircleLogo from "../Circle/CircleLogo";

const MaterialPopUp = ({ className, title, description, date, close }) => {
    return (
        <PopUpContainer className={styles.MaterialPopUp + " " + className}>
            <div className={styles.MaterialPopUpTopBar}>
                <CircleLogo
                    image="/ic_material.svg"
                    className={styles.MaterialCircleLogo}
                />
                <div>
                    <p className={styles.MaterialPopUpTitle}>{title}</p>
                    <p className={styles.MaterialPopUpDate}>{date}</p>
                </div>
            </div>

            <p className={styles.MaterialPopUpDescription}>{description}</p>

            <div className={styles.MatFlexRowEnd}>
                <CancelButton text="Close" onClick={() => close()} />
            </div>
        </PopUpContainer>
    );
};
export default MaterialPopUp;
