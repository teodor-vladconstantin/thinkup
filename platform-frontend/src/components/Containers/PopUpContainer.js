import React from "react";
import styles from "../../../styles/PopUpContainer.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import PopUpOverlay from "../Containers/PopUpOverlay";
import { motion,AnimatePresence } from "framer-motion";


const PopUpContainer = (props) =>{

    const Variants = {
        in: {
            opacity: 1,
            y: "50vh",
        },
        out: {
            opacity: 0,
            y: "-50vh",
        },
    };
    const Transition = {
        type: "tween",
        duration:0.7
    };

    return (
        <PopUpOverlay>
                <motion.div
                initial="out"
                animate="in"
                exit="out"
                variants={Variants}
                transition={Transition}
                key="popUp">
                    <DefaultContainer className={styles.PopUpContainer +" "+props.className} onClick={()=>{}}>
                            {props.children}
                    </DefaultContainer>
                </motion.div>
        </PopUpOverlay>
    )
}
export default PopUpContainer;