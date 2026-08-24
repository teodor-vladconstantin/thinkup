import react from "react";
import styles from '../../../styles/CircleLogo.module.css';
import Image from "next/image";

const CircleLogo = (props) =>{

    return (
        <div className={styles.CircleLogo +' '+props.className}>
            <img src={props.image} className={styles.CircleImage}/>
        </div>
    )
}

export default CircleLogo;