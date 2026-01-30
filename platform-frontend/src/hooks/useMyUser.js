import react, { useState, useEffect } from "react";
import { useUser } from "@auth0/nextjs-auth0";
import axios from "axios";
import { getCustomRoute } from "next/dist/server/server-route-utils";
import { useRouter } from "next/router";
import { verifyText, createUniqueId } from "../utils/utils";

const useMyUser = () => {
    const [User, setUser] = useState(undefined);
    const { user, error, isLoading } = useUser();
    const [myisLoading, setmyisLoading] = useState(false);
    const router = useRouter();

    useEffect(() => {
        if (user != undefined) {
            setmyisLoading(true);
            let id = user.sub.substring(14);
            setUser(
                {
                    name: user.name,
                    email: user.email,
                    description: undefined,
                    picture: user.picture,
                    id: id,
                },
                setmyisLoading(false)
            );
        }
    }, [user]);

    useEffect(() => {
        if (User == undefined) return;
        if (User.description == undefined && User.id != undefined)
            getUserData();
    }, [User]);

    const getUserData = async () => {
        if (User == undefined) return;
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/users/${User.id}`
        );
        //console.log(response.data)
        //console.log(response)
        console.log(response.data);
        console.log(response.data.social_connections);

        if (response.data.id == undefined && user != undefined)
            router.push("/NewAccount");
        else {
            setUser({
                name: response.data.name,
                email: response.data.email,
                description: response.data.description,
                picture: `${process.env.NEXT_PUBLIC_API_URL}/storage/thinkup-profile-picture/${response.data.profile_picture}${response.data.profile_picture_extension}`,
                cover_picture:`${process.env.NEXT_PUBLIC_API_URL}/storage/thinkup-user-cover-images/${response.data.cover_picture}${response.data.cover_picture_extension}`,
                social_connections:{
                    gitHub:response.data.social_connections.gitHub,
                    twitter:response.data.social_connections.twitter,
                    linkedin:response.data.social_connections.linkedin,
                    instagram:response.data.social_connections.instagram,
                    facebook:response.data.social_connections.facebook,
                },
                id: User.id,
                settings: response.data.settings,
                perms: response.data.perms,
            });
        }
        //console.log(response.data)
    };

    const updateUser = (data) => {
        switch (data.case) {
            case "GET":
                getUserData();
                break;
            case "POST":
                addUser(data.data);
                break;
            case "PUT":
                editUser(data.data);
                break;
            case "DELETE":
                deleteUser(data.data);
                break;
            case "LOGOUT":
                logOutUser();
                break;
            default:
                console.log(`Sorry, case doesn't exist.`);
        }
    };

    const logOutUser = () => {
        setUser(undefined);
        router.push("/api/auth/logout");
        localStorage.removeItem("token");
    };
    const deleteUser = async (data) => {};

    const editUser = async (data) => {
        if (!verifyText(data.name, 20) || !verifyText(data.description, 200))
            return;

        const formdata = new FormData();

        const imageId = createUniqueId(),
            imageId2 = createUniqueId();

        formdata.append(
            "json",
            JSON.stringify({
                id: User.id,
                name: data.name,
                description: data.description,
                profile_picture: imageId,
                cover_picture: imageId2,
            })
        );

        formdata.append("file", data.image);
        formdata.append("file2", data.cover_picture);

        const response = await axios.put(
            `${process.env.NEXT_PUBLIC_API_URL}/users/${User.id}`,
            formdata
        );
        if (response.status == 200) {
            await getUserData();
            router.back();
        } else {
            console.log("ERROR");
        }
    };

    const addUser = async (data) => {
        //console.log(data);
        if (!verifyText(data.name, 20) || !verifyText(data.description, 200))
            return;
        const response = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}/users/${User.id}`,
            {
                id: User.id,
                name: data.name,
                email: data.email,
                description: data.description,
                profile_picture: "default",
            }
        );
        if (response.status == 200) {
            await getUserData();
            router.push("/");
        } else {
            console.log("ERROR");
        }
    };

    return [User, updateUser];
};

export default useMyUser;
