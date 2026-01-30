import React from "react";
import styles from "../../../styles/Toggle.module.css";

const Toggle = (props) =>{

    return (
        <label className={styles.Check}>
            <input type="checkbox" className={styles.Toggle} value={props.Language} onChange={()=>props.change()}>
            </input>
            <span className={styles.Slider}></span>
        
        </label>
    )
}

export default Toggle;



                        