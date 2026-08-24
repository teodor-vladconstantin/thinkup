import react from "react";
import styles from '../../../styles/DefaultContainer2.module.css';

const DefaultContainer2 = (props) =>{

    return (
        <div className={styles.DefaultContainer2 +' '+props.className} onClick={()=>props.onClick()}>
            {props.children}
        </div>
    )
}

export default DefaultContainer2;