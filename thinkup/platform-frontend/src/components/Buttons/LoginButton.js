import React from "react";
import { useRouter } from "next/router";
import styles from "../../../styles/LoginButton.module.css";
import axios from "axios";

const LoginButton = () =>{
    const router = useRouter();

    const handleLogin = async () =>{
        const res = await axios.get('https://dev-v37jjjci.us.auth0.com/authorize?response_type=code&client_id=MWmWygbllntrOPhq45d6K0BbF8HoTmhU&redirect_uri=http://127.0.0.1:5000/callback&scope=openid%20profile%20offline_access&state=xyzABC123&audience=https://dev-v37jjjci.us.auth0.com/api/v2/')
        //"api/auth/login"
    }

    //"(https://dev-v37jjjci.us.auth0.com/authorize?response_type=code&client_id=MWmWygbllntrOPhq45d6K0BbF8HoTmhU&redirect_uri=http://localhost:3000/api/callback&scope=openid%20profile%20offline_access&state=xyzABC123&audience=https://dev-v37jjjci.us.auth0.com/api/v2/")
    //Callback auth0:  http://localhost:3000/api/auth/callback


    return (
        <button onClick={()=>router.push("/api/auth/login")} className={styles.LoginButton}>Sign up | Log in</button>
    )
}

export default LoginButton;