import React from "react";
import styles from "../../../styles/DeleteButton.module.css";

const DeleteButton = (props) => {

    return (
        <div className={styles.Container +" " +props.className} onClick={() => props.onClick()} >
            <a>
                {props.text}{props.children!=undefined?" ":""}
                <span>
                    {props.children}
                </span>
            </a>
        </div>
    );
};

export default DeleteButton;
