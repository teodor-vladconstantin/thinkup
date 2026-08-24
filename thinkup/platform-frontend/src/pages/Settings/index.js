import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import styles from "../../../styles/Settings.module.css";
import { useMyUserContext, useMyUserUpdate } from "../../contexts/UserContext";
import DeleteButton from "../../components/Buttons/DeleteButton";
import axios from "axios";
import LinkAccountPopUp from "../../components/PopUp/LinkAccountPopUp";
import { AnimatePresence } from "framer-motion";
import ConfirmationPopUp from "../../components/PopUp/ConfirmationPopUp";
import Toggle from "../../components/FormElems/Toggle";
import AccentButton from "../../components/Buttons/AccentButton";
import CancelButton from "../../components/Buttons/CancelButton";

const Settings = () => {
    const [LinkFacebookPopUp, setLinkFacebookPopUp] = useState(false);
    const [LinkInstagramPopUp, setLinkInstagramPopUp] = useState(false);
    const [LinkLinkedInPopUp, setLinkLinkedInPopUp] = useState(false);
    const [LinkTwitterPopUp, setLinkTwitterPopUp] = useState(false);
    const [LinkGitHubPopUp, setLinkGitHubPopUp] = useState(false);
    const [ConfirmationPopUpLogOut, setConfirmationPopUpLogOut] =
        useState(false);
    const [Language, setLanguage] = useState(false);
    const User = useMyUserContext();
    const updateUser = useMyUserUpdate();
    const router = useRouter();

    useEffect(() => {
        if (User == undefined || User.settings == undefined) return;
        console.log(User.settings.language);
        if (User.settings.language == "ro") setLanguage(true);
        else setLanguage(false);
    }, [User]);

    const saveChanges = async () => {
        const response = await axios.put(
            `${process.env.NEXT_PUBLIC_API_URL}/users/${User.id}/changeLanguage/${
                Language ? "ro" : "en"
            }`
        );
        console.log(response);
        updateUser({
            case: "GET",
            data: {},
        });
        router.back();
    };

    return (
        <div className={styles.Settings}>
            <h1 className={styles.SettingsTitle}>User Settings</h1>
            <div className={styles.LanguageContainer}>
                <p>
                    Language: <span>{Language ? "RO" : "EN"}</span>
                </p>
                <Toggle
                    value={Language}
                    change={() => setLanguage(!Language)}
                ></Toggle>
            </div>
            <h3 className={styles.socialTitle}>Social Links</h3>
            <div className={styles.socialLinks}>
                <p
                    onClick={() => setLinkFacebookPopUp(true)}
                    className={styles.LinkText}
                >
                    <svg
                        width="40"
                        height="45"
                        viewBox="0 0 31 35"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <g clipPath="url(#clip0_45_538)">
                            <path
                                d="M27.1739 2.1875H3.26087C2.39603 2.1875 1.56662 2.5332 0.955087 3.14856C0.343555 3.76391 0 4.59851 0 5.46875L0 29.5312C0 30.4015 0.343555 31.2361 0.955087 31.8514C1.56662 32.4668 2.39603 32.8125 3.26087 32.8125H12.5849V22.4007H8.30503V17.5H12.5849V13.7648C12.5849 9.51631 15.0985 7.16953 18.9484 7.16953C20.7921 7.16953 22.7201 7.50039 22.7201 7.50039V11.6703H20.5958C18.5027 11.6703 17.8499 12.9773 17.8499 14.3179V17.5H22.5224L21.7751 22.4007H17.8499V32.8125H27.1739C28.0387 32.8125 28.8682 32.4668 29.4797 31.8514C30.0912 31.2361 30.4348 30.4015 30.4348 29.5312V5.46875C30.4348 4.59851 30.0912 3.76391 29.4797 3.14856C28.8682 2.5332 28.0387 2.1875 27.1739 2.1875Z"
                                fill="black"
                            />
                        </g>
                        <defs>
                            <clipPath id="clip0_45_538">
                                <rect
                                    width="30.4348"
                                    height="35"
                                    fill="white"
                                />
                            </clipPath>
                        </defs>
                    </svg>
                </p>
                <p
                    onClick={() => setLinkInstagramPopUp(true)}
                    className={styles.LinkText}
                >
                    <svg
                        width="40"
                        height="45"
                        viewBox="0 0 31 35"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <g clipPath="url(#clip0_45_540)">
                            <path
                                d="M15.2244 9.63867C10.9037 9.63867 7.41869 13.1455 7.41869 17.4932C7.41869 21.8408 10.9037 25.3476 15.2244 25.3476C19.545 25.3476 23.0301 21.8408 23.0301 17.4932C23.0301 13.1455 19.545 9.63867 15.2244 9.63867ZM15.2244 22.5996C12.4323 22.5996 10.1497 20.3096 10.1497 17.4932C10.1497 14.6768 12.4255 12.3867 15.2244 12.3867C18.0233 12.3867 20.2991 14.6768 20.2991 17.4932C20.2991 20.3096 18.0165 22.5996 15.2244 22.5996ZM25.17 9.31738C25.17 10.3359 24.3548 11.1494 23.3494 11.1494C22.3372 11.1494 21.5287 10.3291 21.5287 9.31738C21.5287 8.30566 22.344 7.48535 23.3494 7.48535C24.3548 7.48535 25.17 8.30566 25.17 9.31738ZM30.3399 11.1768C30.2244 8.72265 29.6673 6.54883 27.8806 4.75781C26.1007 2.9668 23.9404 2.40625 21.5016 2.2832C18.988 2.13965 11.454 2.13965 8.94042 2.2832C6.50836 2.39941 4.34804 2.95996 2.56135 4.75098C0.774669 6.54199 0.224397 8.71582 0.102114 11.1699C-0.0405486 13.6992 -0.0405486 21.2803 0.102114 23.8096C0.217603 26.2637 0.774669 28.4375 2.56135 30.2285C4.34804 32.0195 6.50157 32.5801 8.94042 32.7031C11.454 32.8467 18.988 32.8467 21.5016 32.7031C23.9404 32.5869 26.1007 32.0264 27.8806 30.2285C29.6605 28.4375 30.2176 26.2637 30.3399 23.8096C30.4825 21.2803 30.4825 13.7061 30.3399 11.1768ZM27.0926 26.5234C26.5627 27.8633 25.5369 28.8955 24.1986 29.4355C22.1945 30.2353 17.4391 30.0508 15.2244 30.0508C13.0097 30.0508 8.24749 30.2285 6.25021 29.4355C4.91869 28.9023 3.89287 27.8701 3.35619 26.5234C2.56135 24.5068 2.74478 19.7217 2.74478 17.4932C2.74478 15.2646 2.56815 10.4727 3.35619 8.46289C3.88608 7.12305 4.91189 6.09082 6.25021 5.55078C8.25428 4.75098 13.0097 4.93555 15.2244 4.93555C17.4391 4.93555 22.2013 4.75781 24.1986 5.55078C25.5301 6.08398 26.5559 7.11621 27.0926 8.46289C27.8874 10.4795 27.704 15.2646 27.704 17.4932C27.704 19.7217 27.8874 24.5137 27.0926 26.5234Z"
                                fill="black"
                            />
                        </g>
                        <defs>
                            <clipPath id="clip0_45_540">
                                <rect
                                    width="30.4348"
                                    height="35"
                                    fill="white"
                                />
                            </clipPath>
                        </defs>
                    </svg>
                </p>
                <p
                    onClick={() => setLinkLinkedInPopUp(true)}
                    className={styles.LinkText}
                >
                    <svg
                        width="40"
                        height="45"
                        viewBox="0 0 31 35"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <g clipPath="url(#clip0_45_542)">
                            <path
                                d="M28.2609 2.1875H2.16712C0.971467 2.1875 0 3.17871 0 4.39551V30.6045C0 31.8213 0.971467 32.8125 2.16712 32.8125H28.2609C29.4565 32.8125 30.4348 31.8213 30.4348 30.6045V4.39551C30.4348 3.17871 29.4565 2.1875 28.2609 2.1875ZM9.19837 28.4375H4.6875V13.8223H9.20516V28.4375H9.19837ZM6.94293 11.8262C5.49592 11.8262 4.32745 10.6436 4.32745 9.19434C4.32745 7.74512 5.49592 6.5625 6.94293 6.5625C8.38315 6.5625 9.55842 7.74512 9.55842 9.19434C9.55842 10.6504 8.38995 11.8262 6.94293 11.8262ZM26.1073 28.4375H21.5965V21.3281C21.5965 19.6328 21.5625 17.4521 19.2527 17.4521C16.9022 17.4521 16.5421 19.2979 16.5421 21.2051V28.4375H12.0312V13.8223H16.3587V15.8184H16.4198C17.0245 14.6699 18.4986 13.46 20.6929 13.46C25.2582 13.46 26.1073 16.4883 26.1073 20.4258V28.4375Z"
                                fill="black"
                            />
                        </g>
                        <defs>
                            <clipPath id="clip0_45_542">
                                <rect
                                    width="30.4348"
                                    height="35"
                                    fill="white"
                                />
                            </clipPath>
                        </defs>
                    </svg>
                </p>
                <p
                    onClick={() => setLinkTwitterPopUp(true)}
                    className={styles.LinkText}
                >
                    <svg
                        width="40"
                        height="45"
                        viewBox="0 0 21 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M18.75 1.5H2.25C1.00781 1.5 0 2.50781 0 3.75V20.25C0 21.4922 1.00781 22.5 2.25 22.5H18.75C19.9922 22.5 21 21.4922 21 20.25V3.75C21 2.50781 19.9922 1.5 18.75 1.5ZM16.4578 8.94375C16.4672 9.075 16.4672 9.21094 16.4672 9.34219C16.4672 13.4062 13.3734 18.0891 7.72031 18.0891C5.97656 18.0891 4.35938 17.5828 3 16.7109C3.24844 16.7391 3.4875 16.7484 3.74063 16.7484C5.17969 16.7484 6.50156 16.2609 7.55625 15.4359C6.20625 15.4078 5.07188 14.5219 4.68281 13.3031C5.15625 13.3734 5.58281 13.3734 6.07031 13.2469C4.66406 12.9609 3.60938 11.7234 3.60938 10.2281V10.1906C4.01719 10.4203 4.49531 10.5609 4.99687 10.5797C4.5752 10.2992 4.22952 9.91869 3.99069 9.4721C3.75186 9.02552 3.6273 8.52675 3.62813 8.02031C3.62813 7.44844 3.77813 6.92344 4.04531 6.46875C5.55938 8.33437 7.83281 9.55313 10.3828 9.68438C9.94687 7.59844 11.5078 5.90625 13.3828 5.90625C14.2687 5.90625 15.0656 6.27656 15.6281 6.87656C16.3219 6.74531 16.9875 6.4875 17.5781 6.13594C17.3484 6.84844 16.8656 7.44844 16.2281 7.82812C16.8469 7.7625 17.4469 7.58906 18 7.35C17.5828 7.96406 17.0578 8.50781 16.4578 8.94375Z"
                            fill="black"
                        />
                    </svg>
                </p>
                <p
                    onClick={() => setLinkGitHubPopUp(true)}
                    className={styles.LinkText}
                >
                    <svg
                        width="45"
                        height="45"
                        viewBox="0 0 35 35"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M17.5 0C7.83125 0 0 7.83125 0 17.5C0 25.2438 5.00938 31.7844 11.9656 34.1031C12.8406 34.2563 13.1687 33.7313 13.1687 33.2719C13.1687 32.8563 13.1469 31.4781 13.1469 30.0125C8.75 30.8219 7.6125 28.9406 7.2625 27.9563C7.06563 27.4531 6.2125 25.9 5.46875 25.4844C4.85625 25.1563 3.98125 24.3469 5.44687 24.325C6.825 24.3031 7.80938 25.5938 8.1375 26.1188C9.7125 28.7656 12.2281 28.0219 13.2344 27.5625C13.3875 26.425 13.8469 25.6594 14.35 25.2219C10.4563 24.7844 6.3875 23.275 6.3875 16.5813C6.3875 14.6781 7.06563 13.1031 8.18125 11.8781C8.00625 11.4406 7.39375 9.64688 8.35625 7.24063C8.35625 7.24063 9.82187 6.78125 13.1687 9.03438C14.5687 8.64063 16.0563 8.44375 17.5438 8.44375C19.0313 8.44375 20.5188 8.64063 21.9188 9.03438C25.2656 6.75938 26.7313 7.24063 26.7313 7.24063C27.6938 9.64688 27.0813 11.4406 26.9063 11.8781C28.0219 13.1031 28.7 14.6563 28.7 16.5813C28.7 23.2969 24.6094 24.7844 20.7156 25.2219C21.35 25.7688 21.8969 26.8187 21.8969 28.4594C21.8969 30.8 21.875 32.6813 21.875 33.2719C21.875 33.7313 22.2031 34.2781 23.0781 34.1031C26.5521 32.9302 29.5709 30.6975 31.7095 27.7191C33.8481 24.7407 34.999 21.1667 35 17.5C35 7.83125 27.1688 0 17.5 0Z"
                            fill="black"
                        />
                    </svg>
                </p>
            </div>

            <DeleteButton
                text="Log out"
                onClick={() => setConfirmationPopUpLogOut(true)}
                className={styles.LogOutbtn}
            />

            <div className={styles.SettingsButtonDiv}>
                <AccentButton text="Save Changes" onClick={() => saveChanges()}>
                    <svg
                        width="21"
                        height="22"
                        viewBox="0 0 21 22"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M1.3125 10.9999C1.3125 10.8259 1.38164 10.6589 1.50471 10.5359C1.62778 10.4128 1.7947 10.3437 1.96875 10.3437H17.4471L13.3166 6.21453C13.1934 6.0913 13.1242 5.92417 13.1242 5.7499C13.1242 5.57564 13.1934 5.40851 13.3166 5.28528C13.4399 5.16205 13.607 5.09283 13.7812 5.09283C13.9555 5.09283 14.1226 5.16205 14.2459 5.28528L19.4959 10.5353C19.557 10.5962 19.6055 10.6687 19.6386 10.7484C19.6716 10.8281 19.6887 10.9136 19.6887 10.9999C19.6887 11.0862 19.6716 11.1717 19.6386 11.2514C19.6055 11.3312 19.557 11.4036 19.4959 11.4645L14.2459 16.7145C14.1226 16.8378 13.9555 16.907 13.7812 16.907C13.607 16.907 13.4399 16.8378 13.3166 16.7145C13.1934 16.5913 13.1242 16.4242 13.1242 16.2499C13.1242 16.0756 13.1934 15.9085 13.3166 15.7853L17.4471 11.6562H1.96875C1.7947 11.6562 1.62778 11.587 1.50471 11.4639C1.38164 11.3409 1.3125 11.174 1.3125 10.9999Z"
                            fill="#888888"
                        />
                    </svg>
                </AccentButton>
                <CancelButton text="Cancel" onClick={() => router.back()} />
            </div>

            <AnimatePresence>
                {ConfirmationPopUpLogOut && (
                    <ConfirmationPopUp
                        message="log out"
                        close={() => setConfirmationPopUpLogOut(false)}
                        confirmed={() =>
                            updateUser({ case: "LOGOUT", data: {} })
                        }
                    />
                )}
                {LinkFacebookPopUp && (
                    <LinkAccountPopUp
                        close={() => setLinkFacebookPopUp(false)}
                        account_type="facebook"
                    />
                )}
                {LinkInstagramPopUp && (
                    <LinkAccountPopUp
                        close={() => setLinkInstagramPopUp(false)}
                        account_type="instagram"
                    />
                )}
                {LinkLinkedInPopUp && (
                    <LinkAccountPopUp
                        close={() => setLinkLinkedInPopUp(false)}
                        account_type="linkedin"
                    />
                )}
                {LinkTwitterPopUp && (
                    <LinkAccountPopUp
                        close={() => setLinkTwitterPopUp(false)}
                        account_type="twitter"
                    />
                )}
                {LinkGitHubPopUp && (
                    <LinkAccountPopUp
                        close={() => setLinkGitHubPopUp(false)}
                        account_type="gitHub"
                    />
                )}
            </AnimatePresence>
        </div>
    );
};

export default Settings;
