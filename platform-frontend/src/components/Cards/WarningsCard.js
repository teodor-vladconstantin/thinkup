import React, { useEffect, useState } from "react";
import styles from "../../../styles/WarningsCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import apiClient from "../../utils/apiClient";

const formatDate = (value) => {
    if (!value) return "";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString();
};

const WarningsCard = (props) => {
    const [Warnings, setWarnings] = useState(undefined);

    const getWarningsData = async () => {
        if (!props.user_id) return;
        try {
            const response = await apiClient.get(
                `${process.env.NEXT_PUBLIC_API_URL}/warnings/student/${props.user_id}`
            );
            setWarnings(response.data.warnings || []);
        } catch (err) {
            console.log(err);
            setWarnings([]);
        }
    };

    useEffect(() => {
        getWarningsData();
    }, [props.user_id]);

    return (
        <DefaultContainer
            style={{ width: props.width }}
            className={styles.WarningsCard + " " + props.className}
            onClick={() => {}}
        >
            <p className={styles.Title}>Avertismente</p>

            {Warnings === undefined ? (
                <p>Se încarcă...</p>
            ) : Warnings.length === 0 ? (
                <p>Niciun avertisment</p>
            ) : (
                <div className={styles.flexDiv}>
                    {Warnings.map((warning) => (
                        <div key={warning.id} className={styles.WarningEntry}>
                            <p className={styles.WarningText}>{warning.text}</p>
                            <p className={styles.WarningDate}>
                                {formatDate(warning.issuedDate)}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </DefaultContainer>
    );
};

export default WarningsCard;
