import os, asyncio
import httpx

AI_API_KEY = os.getenv("AI_API_KEY", "")

async def call_ai_generate(prompt: str) -> str:
    # Placeholder: replace with proper OpenAI client.
    await asyncio.sleep(0.5)
    snippet = (prompt[:900] + "...") if len(prompt) > 900 else prompt
    return f"RÉSUMÉ GÉNÉRIQUE (PLACEHOLDER):\n{snippet}"

def build_prompt(project, activities, tasks):
    prompt = f"Projet: {project.title}\nProgression: {project.progress}%\nDescription: {project.description or ''}\n\nActivités récentes:\n"
    for a in activities[:10]:
        prompt += f"- {a.created_at} — {a.action} — {a.meta}\n"
    prompt += "\nTâches clés:\n"
    for t in tasks[:10]:
        prompt += f"- {t.title} ({t.status})\n"
    prompt += (
        "\nRédige un résumé en français (150-220 mots) organisé en: Contexte, Avancement actuel, "
        "Points bloquants, Prochaines étapes, Recommandation. Ton: professionnel et concis."
    )
    return prompt
