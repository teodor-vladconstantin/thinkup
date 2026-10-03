import react from "react";
import styles from '../../../styles/CircleLogo.module.css';

const CircleLogo = (props) =>{

    return (
        <div className={styles.CircleLogo +' '+props.className}>
            <img alt="" src={props.image} className={styles.CircleImage}/>
        </div>
    )
}

export default CircleLogo;