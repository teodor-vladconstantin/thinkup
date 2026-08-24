import React, { useState, useEffect } from "react";
import styles from "../../../styles/AdminListTable.module.css";
import { useRouter } from "next/router";
import DefaultContainer from "../Containers/DefaultContainer";
import axios from "axios";
import DeleteButton from "../Buttons/DeleteButton";
import AccentButton from "../Buttons/AccentButton";
import CircleAddButton from "../Buttons/CircleAddButton";

const AdminListTable = ({className,adminlist,openPopUp,project_id, refresh}) => {
    /*<div className={styles.ProjectsTableShadow}></div>*/
    const [Users,setUsers] = useState(undefined);

    

    const getUsers = async () =>{

        Promise.all(
            adminlist?.map(async (userID) => {
                const responseU = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/users/${userID}`
                );
                return responseU.data;

            })
        ).then((response) => {
            console.log(response);
            setUsers(response);
        });
    }

    useEffect(()=>{
        console.log(adminlist);
        getUsers();
    },[adminlist])

    const RemoveAdmin = async (user_id) =>{
        //console.log(user_id);
        const response = await axios.delete(`${process.env.NEXT_PUBLIC_API_URL}/projects/${project_id}/admins/${user_id}`);
        console.log(response);
        if(response.status == 200)
            refresh();
    }


    const router = useRouter();

    if (adminlist == undefined) return <></>;

    return (
        
        <DefaultContainer className={styles.AdminListTable} onClick={()=>{}}>
            <div className={styles.AdminListTopBar}>
                <p className={styles.AdminListTitle}>Admin List</p>
                <CircleAddButton onClick={()=>openPopUp()}/>
            </div>
            <div className={styles.AdminListContainer}>
                {
                    Users?.map((user,index)=>{
                        return( 
                            <div className={styles.AdminListCard} key={index}>
                                <div className={styles.AdminUserData} onClick={()=>router.push(`/Profile/${user.id}`)}>
                                    <img className={styles.AdminUserImage} src={`${process.env.NEXT_PUBLIC_API_URL}/storage/thinkup-profile-picture/${user.profile_picture}${user.profile_picture_extension}`}></img>
                                    <p>{user.name}</p>
                                </div>
                                <img src="/user_remove_icon.svg" className={styles.AdminRemoveButton} alt="remove" onClick={()=>RemoveAdmin(user.id)}></img>
                            </div>
                        )
                    })
                }
            </div>

        </DefaultContainer>
    );
};

export default AdminListTable;
