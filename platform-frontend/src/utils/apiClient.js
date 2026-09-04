import axios from "axios";

// Backend routes decorated with @require_auth need a Bearer token.
// /api/token issues a machine-to-machine Auth0 token for the API audience.
const apiClient = axios.create();

let cachedToken = null;
let cachedTokenExpiry = 0;

apiClient.interceptors.request.use(async (config) => {
    if (!cachedToken || Date.now() >= cachedTokenExpiry) {
        const { data } = await axios.get("/api/token");
        cachedToken = data.access_token;
        cachedTokenExpiry = Date.now() + (data.expires_in - 60) * 1000;
    }
    config.headers.Authorization = `Bearer ${cachedToken}`;
    return config;
});

export default apiClient;
