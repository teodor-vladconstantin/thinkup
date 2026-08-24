import react, { useEffect } from "react";
import styles from "../../../styles/CircleProfile.module.css";
import Image from "next/image";

const CircleProfile = (props) => {
    var elem = 0;
    useEffect(() => {
        elem = document.querySelector("." + props.id);
        elem.style.width = props.size;
        var approx_size = Number(props.size[0] + props.size[1]);
        if (approx_size < 5)
            elem.style.border = "2px solid var(--color-accent-primary)";
        else elem.style.border = "4px solid var(--color-accent-primary)";
    });
    return (
        <div
            className={
                styles.CircleProfile + " " + props.className + " " + props.id
            }
            onClick={() => props.onClick()}
        >
            <img src={props.image} className={styles.CircleImage} />
        </div>
    );
};

export default CircleProfile;
