import React, { Children } from "react";
import styles from "../../../styles/UserCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";

const UserCard = (props) =>{

    return (
        <DefaultContainer className={styles.UserCard +" "+props.className} onClick={()=>props.onClick()}>
            <img className={styles.UserCardImage} src={`${process.env.NEXT_PUBLIC_API_URL}/storage/thinkup-profile-picture/${props.profile_picture}${props.profile_picture_extension}`} alt="profile picture"/>
            <p>{props.name}</p>

        </DefaultContainer>
    )
}
export default UserCard;