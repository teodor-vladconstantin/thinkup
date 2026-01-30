import React from "react";
import styles from "../../../styles/AccentButton.module.css";

const AccentButton = (props) => {

    return (
        <div className={styles.Container +" " +props.className}>
            <a onClick={() => props.onClick()}>
                {props.text}{props.children!=undefined?" ":""}
                <span>
                    {props.children}
                </span>
            </a>
        </div>
    );
};

export default AccentButton;
