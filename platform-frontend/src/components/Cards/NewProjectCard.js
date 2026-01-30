import react from "react";
import styles from "../../../styles/NewProjectCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import { motion } from "framer-motion";

const ProjectCard = (props) => {
    const Variants = {
        in: {
            opacity: 1,
            y: "0",
        },
        out: {
            opacity: 0,
            y: "15vh",
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
                className={styles.ProjectCard + " " + props.className}
                onClick={() => props.onClick()}
            >
                <svg width="50" height="50" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M24.7031 14V35.4062M35.4062 24.7031H14H35.4062Z" stroke="#EAEAFF" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
</svg>

            </DefaultContainer>
        </motion.div>
    );
};

export default ProjectCard;
