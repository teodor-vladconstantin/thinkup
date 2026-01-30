import react,{useEffect, useState} from "react";
import styles from "../../../styles/NewAccount.module.css";
import { useUser } from "@auth0/nextjs-auth0";
import InputField from "../../components/FormElems/InputField";
import TextArea from "../../components/FormElems/TextArea";
import AccentButton from "../../components/Buttons/AccentButton";
import CancelButton from "../../components/Buttons/CancelButton";
import axios from "axios";
import { useRouter } from "next/router";
import {useMyUserContext,useMyUserUpdate } from '../../contexts/UserContext'
import  useMyUser  from "../../hooks/useMyUser";

const NewAccount = () =>{
    const [FullName,setFullName] = useState("");
    const [Email,setEmail] = useState("");
    const [Description,setDescription] = useState("");
    const router = useRouter();
    const User = useMyUserContext();
    const updateUser = useMyUserUpdate();

    useEffect(()=>{
        if(User!=undefined){
            setFullName(User.name);
            setEmail(User.email);
        }
    },[User])

    const addUser =() =>{
        updateUser({
            'case':'POST',
            'data':{
                'name':FullName,
                'email':Email,
                'description':Description
            }
        })
    }

    return (
        <form className={styles.NewAccount} onSubmit={(e)=>addUser(e)}>
            <h1 className={styles.NewAccountTitle}>New Account</h1>
            <div className={styles.NewAccountNameDiv}>
                <InputField InputTitle="Full Name" width="325" value={FullName} onChange={(e)=>setFullName(e.target.value)}/>
                <InputField InputTitle="Email" width="325" value={Email} onChange={(e)=>setEmail(e.target.value)}/>
            </div>
            <TextArea
                areaTitle="Description"
                placeholder="Write your description here..."
                subheader="false"
                className={styles.NewAccountDescription}
                value={Description} onChange={(e)=>setDescription(e.target.value)}
                width="675"
            />
            <div className={styles.NewAccountButtonDiv}>
                <AccentButton text="Create" onClick={()=>addUser()}>
                    <svg width="21"height="22"viewBox="0 0 21 22"fill="none"xmlns="http://www.w3.org/2000/svg">
                        <path fillRule="evenodd"clipRule="evenodd"d="M1.3125 10.9999C1.3125 10.8259 1.38164 10.6589 1.50471 10.5359C1.62778 10.4128 1.7947 10.3437 1.96875 10.3437H17.4471L13.3166 6.21453C13.1934 6.0913 13.1242 5.92417 13.1242 5.7499C13.1242 5.57564 13.1934 5.40851 13.3166 5.28528C13.4399 5.16205 13.607 5.09283 13.7812 5.09283C13.9555 5.09283 14.1226 5.16205 14.2459 5.28528L19.4959 10.5353C19.557 10.5962 19.6055 10.6687 19.6386 10.7484C19.6716 10.8281 19.6887 10.9136 19.6887 10.9999C19.6887 11.0862 19.6716 11.1717 19.6386 11.2514C19.6055 11.3312 19.557 11.4036 19.4959 11.4645L14.2459 16.7145C14.1226 16.8378 13.9555 16.907 13.7812 16.907C13.607 16.907 13.4399 16.8378 13.3166 16.7145C13.1934 16.5913 13.1242 16.4242 13.1242 16.2499C13.1242 16.0756 13.1934 15.9085 13.3166 15.7853L17.4471 11.6562H1.96875C1.7947 11.6562 1.62778 11.587 1.50471 11.4639C1.38164 11.3409 1.3125 11.174 1.3125 10.9999Z"fill="#888888"/>
                    </svg>
                </AccentButton>
                <CancelButton text="Cancel"/>
            </div>




        </form>
    )
}

export default NewAccount;