import react, { useState } from "react";
import styles from "../../../styles/FilterComponent.module.css";
import DefaultContainer from "../Containers/DefaultContainer";

const SelectField = (props) => {
    const [FilterState, setFilterState] = useState(false);

    return (
        <div>
            <DefaultContainer className={styles.Container}>
                <div className={styles.titleDiv}>
                    <svg
                        width="19"
                        height="19"
                        viewBox="0 0 19 19"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <rect
                            x="0.625"
                            y="0.625"
                            width="7.19444"
                            height="7.19444"
                            rx="1.375"
                            stroke="#222222"
                            strokeWidth="1.25"
                        />
                        <rect
                            x="11.1804"
                            y="11.1807"
                            width="7.19444"
                            height="7.19444"
                            rx="1.375"
                            stroke="#222222"
                            strokeWidth="1.25"
                        />
                        <rect
                            x="11.1804"
                            y="0.625"
                            width="7.19444"
                            height="7.19444"
                            rx="3.375"
                            stroke="#222222"
                            strokeWidth="1.25"
                        />
                        <rect
                            x="0.625"
                            y="11.1807"
                            width="7.19444"
                            height="7.19444"
                            rx="3.375"
                            stroke="#222222"
                            strokeWidth="1.25"
                        />
                    </svg>
                    <h3>Category</h3>
                </div>
            </DefaultContainer>

            <DefaultContainer
                className={
                    styles.FilterComponent +
                    " " +
                    props.className +
                    " " +
                    styles.Accent
                }
                onClick={() => setFilterState(!FilterState)}
            >
                <div className={styles.TopFilter}>
                    <p>{props.value}</p>
                    <img src="/ls_dropdown.svg" />
                </div>
                <div
                    className={
                        FilterState
                            ? styles.FilterValuesDiv +
                              " " +
                              styles.FilterVisible
                            : styles.FilterValuesDiv
                    }
                >
                    {props.options?.map((option, index) => {
                        return (
                            <p
                                onClick={() => props.setValue(option)}
                                key={index}
                            >
                                {option}
                            </p>
                        );
                    })}
                </div>
            </DefaultContainer>
        </div>
    );
};

export default SelectField;
