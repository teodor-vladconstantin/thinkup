import react from "react";
import styles from '../../../styles/PopUpOverlay.module.css';
import {motion} from 'framer-motion'

const PopUpOverlay = (props) =>{

    return (
        <motion.div className={styles.PopUpOverlay +' '+props.className}>
            {props.children}
        </motion.div>
    )
}

export default PopUpOverlay;