import React from "react";
import styles from "../../../styles/CircleAddButton.module.css";

const CircleAddButton = (props) => {

    return (
        <div className={styles.CircleAddButton+' '+props.className} onClick={()=>props.onClick()}>
            <svg
                width="50"
                height="50"
                viewBox="0 0 50 50"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    d="M24.7031 14V35.4062M35.4062 24.7031H14H35.4062Z"
                    stroke="#eaeaff"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            </svg>
        </div>
    );
};

export default CircleAddButton;
