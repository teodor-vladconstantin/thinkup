import React from "react";
import styles from "../../../styles/CategoryCard.module.css";

const CategoryCard = (props) => {
    return (
        <div
            className={
                styles.CategoryCard +
                " " +
                props.className +
                " " +
                styles["ChallengeColor" + (props.colorIndex ?? 0)]
            }
            onClick={() => {}}
        >
            {props.children}
        </div>
    );
};
export default CategoryCard;
