import react, { useEffect, useState } from "react";
import styles from "../../../styles/EditUser.module.css";
import { useUser } from "@auth0/nextjs-auth0";
import InputField from "../../components/FormElems/InputField";
import TextArea from "../../components/FormElems/TextArea";
import AccentButton from "../../components/Buttons/AccentButton";
import CancelButton from "../../components/Buttons/CancelButton";
import axios from "axios";
import { useRouter } from "next/router";
import { useMyUserContext, useMyUserUpdate } from "../../contexts/UserContext";
import { route } from "next/dist/server/router";
import ImageInput from "../../components/FormElems/ImageInput";
import FormData from "form-data";
import ScrollContainer from "../../components/Containers/ScrollContainer";

const EditUser = () => {
    const [FullName, setFullName] = useState("");
    const [Description, setDescription] = useState("");
    const [File, setFile] = useState(null);
    const [CoverFile, setCoverFile] = useState(null);

    const User = useMyUserContext();
    const updateUser = useMyUserUpdate();

    const router = useRouter();

    useEffect(() => {
        if (User != undefined) {
            setFullName(User.name);
            setDescription(User.description);
        }
    }, [User]);

    const EditUser = () => {
        updateUser({
            case: "PUT",
            data: {
                name: FullName,
                description: Description,
                image: File,
                cover_picture: CoverFile,
            },
        });
    };

    const PushImagetoDatabase = async () => {
        let data = new FormData();
        data.append("file", SelectedFile, "profileimage");
        const response = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}/photo/123`,
            data
        );
        console.log(response);
    };

    const handleFileChange = (e) => {
        const [f] = e.target.files;
        setFile(f);
    };

    const handleCoverChange = (e) => {
        const [f] = e.target.files;
        setCoverFile(f);
        console.log(CoverFile);
    };

    return (
        <ScrollContainer>
            <div className={styles.EditUser}>
                <h1 className={styles.EditUserTitle}>Edit Account</h1>
                <div className={styles.EditUserNameDiv}>
                    <InputField
                        InputTitle="Full Name"
                        width="675"
                        value={FullName}
                        onChange={(e) => setFullName(e.target.value)}
                    />
                </div>
                <ImageInput
                    setSelectedFile={(file) => handleFileChange(file)}
                    InputTitle="Profile Picture"
                />
                <ImageInput
                    setSelectedFile={(file) => handleCoverChange(file)}
                    InputTitle="Cover Picture"
                />
                <TextArea
                    areaTitle="Description"
                    placeholder="Write your description here..."
                    subheader="false"
                    className={styles.EditUserDescription}
                    value={Description}
                    onChange={(e) => setDescription(e.target.value)}
                    width="675"
                />
                <div className={styles.EditUserButtonDiv}>
                    <AccentButton text="Save" onClick={() => EditUser()}>
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
            </div>
        </ScrollContainer>
    );
};

export default EditUser;
