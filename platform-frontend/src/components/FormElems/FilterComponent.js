import react, { useState } from "react";
import styles from "../../../styles/FilterComponent.module.css";
import DefaultContainer from "../Containers/DefaultContainer";

const FilterComponent = (props) => {
    const [FilterState, setFilterState] = useState(false);

    return (
        <DefaultContainer
            className={styles.FilterComponent + " " + props.className}
            onClick={() => setFilterState(!FilterState)}
        >
            <div className={styles.TopFilter}>
                <p>{props.value}</p>
                <img src="ls_dropdown.svg" />
            </div>
            <div
                className={
                    FilterState
                        ? styles.FilterValuesDiv + " " + styles.FilterVisible
                        : styles.FilterValuesDiv
                }
            >
                <p onClick={() => props.setValue("Filter")}>None</p>
                {props.options?.map((option, index) => {
                    return (
                        <p onClick={() => props.setValue(option)} key={index}>
                            {option}
                        </p>
                    );
                })}
            </div>
        </DefaultContainer>
    );
};

export default FilterComponent;
