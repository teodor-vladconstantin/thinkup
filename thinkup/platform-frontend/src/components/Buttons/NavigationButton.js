import react from "react";
import styles from "../../../styles/NavigationButton.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import Image from "next/image";
import { motion } from "framer-motion";

const NavigationButton = (props) => {
    //<Image src={"/"+props.icon} className={styles.NavigationButtonIcon} alt="icon" width={30} height={30}/>

    const Variants = {
        in: {
            opacity: 1,
            x: "0",
        },
        out: {
            opacity: 0,
            x: "-5vw",
        },
    };
    const Transition = {
        type: "tween",
        ease: "circOut",
        delay: props.animation_delay / 6,
        duration: 2,
    };

    return (
        <motion.div
            initial="out"
            animate="in"
            exit="out"
            variants={Variants}
            transition={Transition}
        >
            <DefaultContainer
                className={
                    (props.selected ? styles.NavigationButtonSelected : "") +
                    " " +
                    styles.NavigationButton +
                    " " +
                    props.className
                }
                onClick={() => props.onClick()}
            >
                {props.children}
            </DefaultContainer>
        </motion.div>
    );
};

export default NavigationButton;
