import react from "react";
import styles from "../../../styles/NewMaterialCard.module.css";
import CircleAddButton from "../Buttons/CircleAddButton";
import DefaultContainer2 from "../Containers/DefaultContainer2";

const NewMaterialCard = (props) => {
    return (
        <DefaultContainer2
            className={styles.NewMaterialCard + " " + props.className}
            onClick={() => props.onClick()}
        >

            <CircleAddButton className={styles.MaterialAddButton} onClick={()=>{}}/>

            <h2 className={styles.NewMaterialText}>{props.children}</h2>
        </DefaultContainer2>
    );
};

export default NewMaterialCard;
