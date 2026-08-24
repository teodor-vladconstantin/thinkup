import react from "react";
import styles from '../../../styles/DefaultContainer.module.css';

const DefaultContainer = (props) =>{

    return (
        <div className={styles.DefaultContainer +' '+props.className} onClick={props.onClick} style={props.style}>
            {props.children}
        </div>
    )
}

export default DefaultContainer;