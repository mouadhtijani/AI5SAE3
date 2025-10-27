# backend/app/tasks.py
from datetime import datetime
from .database import SessionLocal
from . import models
import traceback

def _fmt_dt(dt):
    try:
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return str(dt or "")

def build_local_summary(project, activities, tasks_list):
    lines = []
    lines.append("RÉSUMÉ GÉNÉRIQUE (PLACEHOLDER) :")
    lines.append(f"Projet: {project.title}")
    lines.append(f"Progression: {project.progress}%")
    if project.description:
        lines.append(f"Description: {project.description}")
    lines.append("")
    lines.append("Activités récentes :")
    if activities:
        for a in activities[:6]:
            ts = _fmt_dt(getattr(a, "created_at", None))
            lines.append(f"- {ts} — {getattr(a,'action', '')}")
    else:
        lines.append("- Aucune activité enregistrée.")
    lines.append("")
    lines.append("Tâches importantes :")
    if tasks_list:
        for t in tasks_list[:6]:
            lines.append(f"- {getattr(t,'title','untitled')} ({getattr(t,'status','unknown')})")
    else:
        lines.append("- Aucune tâche enregistrée.")
    lines.append("")
    lines.append("Conclusion & prochaines étapes :")
    try:
        prog = int(getattr(project, "progress", 0) or 0)
    except:
        prog = 0
    if prog >= 80:
        lines.append("Le projet est bien avancé. Finaliser tests et documentation, préparer soutenance.")
    elif prog >= 40:
        lines.append("Avancement moyen. Consolider les fonctionnalités clés et régler les blocages.")
    else:
        lines.append("Début de projet. Prioriser architecture, tâches critiques et répartition d'équipe.")
    lines.append("")
    lines.append("Recommandations :")
    lines.append("- Faire une revue de code hebdomadaire.")
    lines.append("- Mettre à jour planning et livrables.")
    return "\n".join(lines)

def generate_summary_sync(project_id: int):
    """
    Génération synchronisée : construit le texte, l'enregistre en DB et renvoie le contenu.
    Retour: {"ok": True, "content": "...", "summary_id": id} ou {"ok": False, "error": "..."}
    """
    db = SessionLocal()
    try:
        print(f"[tasks] generate_summary_sync start project_id={project_id}")
        project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if not project:
            err = "project not found"
            print("[tasks] ERROR:", err)
            return {"ok": False, "error": err}

        activities = []
        if hasattr(models, "Activity"):
            activities = db.query(models.Activity).filter(models.Activity.project_id == project_id) \
                .order_by(models.Activity.created_at.desc()).all()

        tasks_list = []
        if hasattr(models, "Task"):
            tasks_list = db.query(models.Task).filter(models.Task.project_id == project_id) \
                .order_by(models.Task.updated_at.desc()).all()

        content = build_local_summary(project, activities, tasks_list)
        print("[tasks] Built summary (len):", len(content))

        # save summary
        summary = models.Summary(
            project_id=project_id,
            content=content,
            generated_at=datetime.utcnow(),
            version=(getattr(project, "version", 0) + 1)
        )
        db.add(summary)
        db.commit()
        db.refresh(summary)
        print(f"[tasks] Saved summary id={summary.id}")

        # return
        return {"ok": True, "content": content, "summary_id": summary.id}
    except Exception as e:
        db.rollback()
        print("[tasks] Exception:", e)
        traceback.print_exc()
        return {"ok": False, "error": str(e)}
    finally:
        db.close()
        print(f"[tasks] generate_summary_sync end project_id={project_id}")
