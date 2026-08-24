import react from "react";
import styles from '../../../styles/ScrollContainer.module.css';

const ScrollContainer = (props) =>{

    return (
        <div className={styles.ScrollContainer +' '+props.className}>
            {props.children}
            <div className={styles.scrollbarTop}></div>
        </div>
    )
}

export default ScrollContainer;