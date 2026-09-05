import axios from "axios";

// Backend routes decorated with @require_auth need a Bearer token.
// /api/token issues the current logged-in user's own Auth0 access token
// (401 if there's no active session) - not a machine-to-machine token.
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
