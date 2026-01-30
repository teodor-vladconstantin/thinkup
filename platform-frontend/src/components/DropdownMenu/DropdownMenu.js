import React, { useState } from "react";
import styles from "../../../styles/DropDownMenu.module.css";

const DropDownMenu = (props) =>{
    const [MenuState,setMenuState] = useState(false);

    return (
        <div className={styles.DropDownMenu}>
            <img src="/3dots-icon.svg" alt="3 dots" onClick={()=>props.setMenuState(!props.MenuState)} className={styles.DropDownMenuBtn}/>
            {props.MenuState?
            <div className={styles.DropDownMenuOptions}>
                {
                    props.options?.map((option,index)=>{
                        return <p className={styles.DropDownMenuLinks} key={index} onClick={()=>props.optionClick(option)}>{option}</p>
                    })
                }
            </div>
            :<></>}
        </div>
    )
}

export default DropDownMenu;