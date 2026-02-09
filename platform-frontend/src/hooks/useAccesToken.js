import react, { useState, useEffect } from "react";
import { useUser } from "@auth0/nextjs-auth0";
import axios from "axios";

const useAccesToken = () => {
  const [AccesToken, setAccesToken] = useState("");
  const { user, error, isLoading } = useUser();

  const getToken = async () => {
    let response = await axios.get("/api/token");
    return response.data.access_token;
  }

  useEffect(() => {
    const fetchToken = async () => {
      if (user != undefined) {
        try {
          const temp_tok = await getToken();
          setAccesToken(temp_tok);
        } catch (e) {
          console.error("Error fetching token:", e);
        }
      }
      else {
        setAccesToken("");
      }
    };
    fetchToken();
  }, [user]);

  return AccesToken;
};

export default useAccesToken;
