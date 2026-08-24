import react, { useState, useEffect } from "react";
import styles from "../../../styles/MaterialCard.module.css";
import CircleLogo from "../Circle/CircleLogo";
import DefaultContainer2 from "../Containers/DefaultContainer2";
import DropDownMenu from "../DropdownMenu/DropdownMenu";
import axios from "axios";

const MaterialCard = (props) => {
    const [MenuOptions, setMenuOptions] = useState();

    const setMenuState = (newstate) => {
        if (newstate) props.openMenu();
        else props.closeMenu();
    };

    useEffect(() => {
        console.log(props.nrofmaterials);
        if (props.index == 0)
            setMenuOptions(new Array("move down", "edit", "delete"));
        else if (props.index + 1 == props.nrofmaterials)
            setMenuOptions(new Array("move up", "edit", "delete"));
        else
            setMenuOptions(new Array("move up", "move down", "edit", "delete"));
    }, []);

    const deleteMaterial = async () => {
        //console.log(props);
        const response = await axios.delete(
            `${process.env.NEXT_PUBLIC_API_URL}/materials/${props.id}`
        );
        if (response.status == 200) {
            console.log("DELETED");
            props.refresh();
        } else {
            console.log("ERROR");
        }
    };

    const moveUP = async () => {
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/materials/move/up/${props.id}`
        );
        if (response.status == 200) {
            console.log("MOVED");
            props.refresh();
        } else {
            console.log("ERROR");
        }
    };

    const moveDOWN = async () => {
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/materials/move/down/${props.id}`
        );
        if (response.status == 200) {
            console.log("MOVED");
            props.refresh();
        } else {
            console.log("ERROR");
        }
    };

    const HandleClick = (option) => {
        switch (option) {
            case "move up":
                moveUP();
                break;
            case "move down":
                moveDOWN();
                break;
            case "edit":
                console.log("edit");
                break;
            case "delete":
                deleteMaterial();
                break;
            default:
                break;
        }
    };

    return (
        <DefaultContainer2
            className={styles.MaterialCard + " " + props.className}
            onClick={() => {}}
        >
            <CircleLogo image="/ic_material.svg" />
            <div
                className={styles.MaterialCardTextContainer}
                onClick={() => props.onClick()}
            >
                <h2 className={styles.MaterialCardTitle}>{props.title}</h2>
                <p className={styles.MaterialCardDate}>{props.date}</p>
            </div>
            <DropDownMenu
                options={MenuOptions}
                optionClick={(option) => HandleClick(option)}
                MenuState={props.MenuState}
                setMenuState={(newstate) => setMenuState(newstate)}
            />
        </DefaultContainer2>
    );
};

export default MaterialCard;
