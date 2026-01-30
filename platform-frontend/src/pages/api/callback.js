import axios from "axios";
import qs from 'qs';
import cookie from 'cookie';

export default async function handler(req, res) {
    console.log(req.query.code);
    const new_code = req.query.code;
    const params = new URLSearchParams();
    //params.append('application/x-www-form-urlencoded','value1');
    params.append('grant_type', 'authorization_code');
    params.append('client_id', 'MWmWygbllntrOPhq45d6K0BbF8HoTmhU');
    params.append('client_secret', 'G0MndWebolbolF7pCp6eRH27CtwRUVMheC5pSJWw_2yCC9hbtgezrmBLiuBZpTFi');
    params.append('code', new_code);
    params.append('redirect_uri', 'http://localhost:3000/api/callback');

    const data = {
        'grant_type':'authorization_code',
        'client_id': 'MWmWygbllntrOPhq45d6K0BbF8HoTmhU',
        'client_secret': 'G0MndWebolbolF7pCp6eRH27CtwRUVMheC5pSJWw_2yCC9hbtgezrmBLiuBZpTFi',
        'code': new_code,
        'redirect_uri': 'http://localhost:3000/api/callback'
    }


    const options = {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(data),
        url:"https://dev-v37jjjci.us.auth0.com/oauth/token"
      };

    const token_data = await axios(options);
    console.log(token_data.data);
    
    //res.cookie("hello", token_data);

    res.setHeader("Set-Cookie",cookie.serialize("tokens",token_data.data))

    res.redirect(307, '/');
}