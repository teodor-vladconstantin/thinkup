import React, { Children } from "react";
import styles from "../../../styles/TitleInputField.module.css";

const TitleInputField = (props) =>{

    return <input className={styles.TitleInputField} type="text" placeholder={props.placeholder} value={props.value} onChange={(e)=>props.onChange(e)}/>
}

export default TitleInputField;



                        