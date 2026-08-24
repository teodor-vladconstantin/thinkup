import axios from 'axios';

export default async function handler(req, res) {
  try {
    const issuerBaseUrl = process.env.AUTH0_ISSUER_BASE_URL.replace(/\/$/, '');
    const response = await axios.post(`${issuerBaseUrl}/oauth/token`, {
      client_id: process.env.AUTH0_CLIENT_ID,
      client_secret: process.env.AUTH0_CLIENT_SECRET,
      audience: process.env.AUTH0_AUDIENCE,
      grant_type: "client_credentials"
    });
    res.status(200).json(response.data);
  } catch (error) {
    console.error("Token fetch error:", error.response?.data || error.message);
    res.status(error.response?.status || 500).json({ error: error.message });
  }
}
