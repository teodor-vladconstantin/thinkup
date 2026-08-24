import react from "react";
import styles from "../../../styles/NewGoalCard.module.css";
import CircleAddButton from "../Buttons/CircleAddButton";
import DefaultContainer2 from "../Containers/DefaultContainer2";

const NewObjectiveCard = (props) => {
    return (
        <DefaultContainer2
            className={styles.NewGoalCard + " " + props.className}
            onClick={() => props.onClick()}

        >
            <CircleAddButton className={styles.GoalAddButton} onClick={()=>{}}/>
            <h2 className={styles.NewGoalText}>Add a new objective</h2>
        </DefaultContainer2>
    );
};

export default NewObjectiveCard;

