import { getAccessToken, getSession, AccessTokenError } from '@auth0/nextjs-auth0';

export default async function handler(req, res) {
  try {
    const session = getSession(req, res);
    if (!session) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    const { accessToken } = await getAccessToken(req, res);
    const expiresIn = session.accessTokenExpiresAt
      ? session.accessTokenExpiresAt - Math.floor(Date.now() / 1000)
      : 3600;

    res.status(200).json({ access_token: accessToken, expires_in: expiresIn });
  } catch (error) {
    if (error instanceof AccessTokenError) {
      console.error("Token fetch error (no valid user session):", error.code, error.message);
      return res.status(401).json({ error: 'Not authenticated' });
    }
    console.error("Token fetch error:", error.message);
    res.status(500).json({ error: error.message });
  }
}
