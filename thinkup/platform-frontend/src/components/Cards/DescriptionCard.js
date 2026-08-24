import React, { Children } from "react";
import styles from "../../../styles/DescriptionCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";

const DescriptionCard = ({className , children , language}) =>{
    return (
        <DefaultContainer className={styles.DescriptionCard +" "+className} onClick={()=>{}}>
            <p className={styles.DescriptionTitle}>{language=="ro"?"Descriere":"Description"}</p>
            <p className={styles.DescriptionText}>{children}</p>
        </DefaultContainer>
    )
}
export default DescriptionCard;