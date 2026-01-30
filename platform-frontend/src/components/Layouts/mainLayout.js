import react from "react";
import Head from "next/head";
import styles from "../../../styles/MainLayout.module.css";
import { ThemeProvider } from "../../contexts/ThemeContext";
import { UserProvider } from "@auth0/nextjs-auth0";
import NavBar from "../Navigation/NavBar";
import TopBar from "../Navigation/TopBar";
import { MyUserProvider } from "../../contexts/UserContext";
import { AccesTokenProvider } from "../../contexts/AccesTokenContext";

const MainLayout = ({ children }) => {
    return (
        <>
            {/*<Head>
                <meta httpEquiv="Content-Security-Policy" content="upgrade-insecure-requests"/>
    </Head>*/}

            <UserProvider>
                <MyUserProvider>
                    <AccesTokenProvider>
                        <ThemeProvider>
                            <div className={styles.MainLayoutBackground}>
                                <div className={styles.MainLayout}>
                                    <TopBar
                                        user_name="Vana Marc"
                                        user_account="student"
                                        user_image="testing_profile_image.jpg"
                                    />
                                    <div className={styles.MainLayoutContainer}>
                                        <NavBar />
                                        {children}
                                    </div>
                                </div>
                            </div>
                        </ThemeProvider>
                    </AccesTokenProvider>
                </MyUserProvider>
            </UserProvider>
        </>
    );
};

export default MainLayout;
