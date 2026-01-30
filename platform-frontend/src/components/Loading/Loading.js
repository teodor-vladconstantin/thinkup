import React from "react";
import styles from "../../../styles/Loading.module.css";

const Loading = (props) => {

    return (
        <div className={styles.Loading +" " +props.className}>
            <div className={styles.dot}/>
            <div className={styles.dot}/>
            <div className={styles.dot}/>
        </div>
    );
};

export default Loading;
