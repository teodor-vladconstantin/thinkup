import react, { useEffect } from "react";
import styles from "../../../styles/TopBar.module.css";
import ThemeButton from "../Buttons/ThemeButton";
import CircleProfile from "../Circle/CircleProfile";
import { motion } from "framer-motion";
import { useTheme } from "../../contexts/ThemeContext";
import { useUser } from "@auth0/nextjs-auth0";
import { useRouter } from "next/router";
import LoginButton from "../Buttons/LoginButton";
import AccentButton from "../Buttons/AccentButton";
import { useMyUserContext } from "../../contexts/UserContext";

const TopBar = (props) => {
    const Theme = useTheme();
    const router = useRouter();
    const User = useMyUserContext();

    const Variants = {
        in: {
            opacity: 1,
            y: "0",
        },
        out: {
            opacity: 0,
            y: "-5vh",
        },
    };
    const Transition = {
        type: "tween",
        ease: "circOut",
        duration: 2,
    };
    //<ThemeButton className={styles.TopBar_ThemeButton} />

    return (
        <motion.div
            className={styles.TopBar + " " + props.className}
            initial="out"
            animate="in"
            exit="out"
            variants={Variants}
            transition={Transition}
        >
            {Theme ? (
                <img src="/Logo_white.svg" className={styles.TopBar_Logo} />
            ) : (
                <img src="/Logo.svg" className={styles.TopBar_Logo} />
            )}

            <div className={styles.TopBar_LeftSection}>

                {User != undefined ? (
                    <div className={styles.TopBar_UserInfo}>
                        <p className={styles.TopBar_UserName}>{User.name}</p>
                        <p className={styles.TopBar_UserAccount}>
                            {props.user_account}
                        </p>
                    </div>
                ) : (
                    <LoginButton />
                )}

                {User != undefined ? (
                    <CircleProfile
                        image={User.picture}
                        size="3.5rem"
                        id="profilePicture1"
                        onClick={() => router.push(`/Profile/${User.id}`)}
                    />
                ) : (
                    <></>
                )}
            </div>
        </motion.div>
    );
};

export default TopBar;
