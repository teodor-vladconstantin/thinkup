import { handleAuth, handleLogin ,handleCallback } from '@auth0/nextjs-auth0';


const afterCallback = (req, res, session, state) => session;


export default handleAuth({
  async callback(req, res) {
    try {
      await handleCallback(req, res, { afterCallback });
    } catch (error) {
      res.status(error.status || 500).end(error.message);
    }
  }
});

