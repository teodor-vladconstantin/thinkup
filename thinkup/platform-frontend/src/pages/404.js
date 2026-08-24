import React,{useState,useEffect}  from "react";
import styles from "../../styles/MyProfile.module.css";
import { useRouter } from "next/router";
import { useMyUserContext, useMyUserUpdate } from "../contexts/UserContext";
import ScrollContainer from "../components/Containers/ScrollContainer";

export default function FourOhFour() {
    const [Language,setLanguage] = useState("en");
    const User = useMyUserContext();

    const router = useRouter();

    const messages ={
        "en":{
            error:"404 ERROR.",
            message:"Sorry, what you're looking for doesn't exist.",
            home_link:"Go back home."

        },
        "ro":{
            error:"EROARE 404.",
            message:"Scuze,ceea ce cauti nu exista.",
            home_link:"Mergi acasa."
        }
    }

    useEffect(()=>{
        if(User!=undefined && User.settings!=undefined)
            setLanguage(User.settings.language);

    },[User])


    return (
        <ScrollContainer className={styles.noUser}>
            <style jsx>{`
                a {
                    cursor: pointer;
                    font-weight: 500;
                }
            `}</style>
            <h1>{Language=="ro"?messages.ro.error:messages.en.error}</h1>
            <p>
                {Language=="ro"?messages.ro.message:messages.en.message}{" "}
                <span>
                    <a onClick={() => router.push("/")}>{Language=="ro"?messages.ro.home_link:messages.en.home_link}</a>
                </span>
            </p>
        </ScrollContainer>
    );
}
