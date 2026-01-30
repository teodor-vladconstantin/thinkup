import react, { useState, useEffect } from "react";
import { useUser } from "@auth0/nextjs-auth0";
import axios from "axios";

const useAccesToken = () => {
  const [AccesToken, setAccesToken] = useState("");
  const { user, error, isLoading } = useUser();

  const getToken = async () => {
    let response = await axios.post("https://dev-v37jjjci.us.auth0.com/oauth/token", {
      client_id: "MWmWygbllntrOPhq45d6K0BbF8HoTmhU",
      client_secret: "G0MndWebolbolF7pCp6eRH27CtwRUVMheC5pSJWw_2yCC9hbtgezrmBLiuBZpTFi",
      audience: "https://test-api/api",
      grant_type: "client_credentials"
    });
    return response.data.access_token;
  }

  useEffect(async () => {
    if (user != undefined) {
      let temp_tok = await getToken();
      setAccesToken(temp_tok);
      //axios.defaults.headers.common['authorization'] = 'Bearer ' + temp_tok
        /* response = await axios.post("https://dev-v37jjjci.us.auth0.com/oauth/token",{
            "client_id":"MWmWygbllntrOPhq45d6K0BbF8HoTmhU",
            "client_secret":"G0MndWebolbolF7pCp6eRH27CtwRUVMheC5pSJWw_2yCC9hbtgezrmBLiuBZpTFi",
            "audience":"https://test-api/api",
            "grant_type":"client_credentials"
            });

        /*const response = await axios.post("https://dev-v37jjjci.us.auth0.com/oauth/token",{
            "client_id":"MWmWygbllntrOPhq45d6K0BbF8HoTmhU",
            "client_secret":"G0MndWebolbolF7pCp6eRH27CtwRUVMheC5pSJWw_2yCC9hbtgezrmBLiuBZpTFi",
            "audience":"https://test-api/api",
            "grant_type":"authorization_code",
            "redirect_uri":"http://localhost:3000/api/auth/callback"
            });*/


        // console.log("token response", response);
        return("response.data.access_token")
    }
    else {
      setAccesToken("");
      //axios.defaults.headers.common['authorization'] = ''
    }
  }, [user]);

  return AccesToken;
};

export default useAccesToken;