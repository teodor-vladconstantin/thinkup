import react, { useState, useEffect } from "react";
import Head from "next/head";
import styles from "../../../styles/Contact.module.css";
import InputField from "../../components/FormElems/InputField";
import SelectField from "../../components/FormElems/SelectField";
import TextArea from "../../components/FormElems/TextArea";
import AccentButton from "../../components/Buttons/AccentButton";
import CancelButton from "../../components/Buttons/CancelButton";
import { useRouter } from "next/router";
import ScrollContainer from "../../components/Containers/ScrollContainer";
import axios from "axios";
import { useMyUserContext } from "../../contexts/UserContext";
import FilterComponent from "../../components/FormElems/FilterComponent.js";

const Contact = () => {
    const [FullName, setFullName] = useState("");
    const [Email, setEmail] = useState("");
    const [Message, setMessage] = useState("");
    const [AreaOfImplementation, setAreaOfImplementation] = useState("0");
    const [Language, setLanguage] = useState("en");
    const User = useMyUserContext();
    const AreaOfImplementationOptions = new Array(
        "Question",
        "Feedback",
        "Report issue"
    );
    const [FilterValue, setFilterValue] = useState("Select");

    const messages = {
        en: {
            title: "Contact Us",
            description: "We'll get back to you as soon as possible.",
        },
        ro: {
            title: "Contactează-ne",
            description: "Vă vom răspunde în cel mai scurt timp.",
        },
    };

    const router = useRouter();
    const RouteTo = (new_route) => {
        console.log(router.pathname);
        router.push(new_route);
    };

    const sendEmail = async () => {
        const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/contact`, {
            fullname: FullName,
            email: Email,
            message: Message,
        });
        console.log(response);
        if (response.statusText == "OK") {
            document.querySelector(".successful").style.display = "block";
            setTimeout(() => {
                document.querySelector(".successful").style.display = "none";
            }, 5000);
        } else {
            document.querySelector(".error").style.display = "block";
            setTimeout(() => {
                document.querySelector(".error").style.display = "none";
            }, 5000);
        }
    };

    useEffect(() => {
        if (User != undefined && User.settings != undefined)
            setLanguage(User.settings.language);
    }, [User]);

    return (
        <ScrollContainer className={styles.Contact}>
            <Head>
                <title>ThinkUp Academy</title>
                <meta name="description" content="Platfoma ThinkUp" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <h1>{Language == "ro" ? messages.ro.title : messages.en.title}</h1>
            <h4>
                {Language == "ro"
                    ? messages.ro.description
                    : messages.en.description}
            </h4>
            <div className={styles.formLine}>
                <InputField
                    InputTitle="Full Name"
                    width="250"
                    value={FullName}
                    onChange={(e) => setFullName(e.target.value)}
                />
                <InputField
                    InputTitle="Email"
                    width="350"
                    value={Email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <SelectField
                value={FilterValue}
                setValue={(e) => setFilterValue(e)}
                options={AreaOfImplementationOptions}
            />
            <TextArea
                areaTitle="Your Message"
                width="675"
                placeholder="Type freely your message here..."
                subHeader="false"
                value={Message}
                onChange={(e) => setMessage(e.target.value)}
            />
            <div className={styles.btnDiv}>
                <AccentButton text="Submit" onClick={() => sendEmail()}>
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
                <CancelButton text="Cancel" onClick={() => RouteTo("/")} />
            </div>
            <div className={styles.successful + " successful"}>Thank you!</div>
            <div className={styles.error + " error"}>
                There was an error, please try again.
            </div>
        </ScrollContainer>
    );
};

export default Contact;
