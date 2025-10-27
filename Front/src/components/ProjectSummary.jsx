import axios from "axios";
const API = axios.create({ baseURL: process.env.REACT_APP_API_URL || "http://127.0.0.1:8000" });

async function generateAndFetch(projectId, setSummary, addNotification, setLoading){
  setLoading(true);
  try{
    const post = await API.post(`/projects/${projectId}/summaries/generate`);
    const data = post.data || {};
    // si backend renvoie le résumé directement
    const direct = data.summary ?? data.content ?? null;
    if(direct){
      setSummary(direct);
      addNotification("Résumé généré !");
      return;
    }
    // sinon polling (si backend fait background)
    for(let i=0;i<8;i++){
      await new Promise(r=>setTimeout(r, 500));
      const latest = await API.get(`/projects/${projectId}/summaries/latest`);
      const got = latest.data?.summary ?? latest.data?.content ?? null;
      if(got){
        setSummary(got);
        addNotification("Résumé récupéré !");
        return;
      }
    }
    addNotification("Résumé en cours de génération, réessayez dans quelques instants.");
  }catch(e){
    console.error(e);
    addNotification("Erreur génération");
  } finally {
    setLoading(false);
  }
}
