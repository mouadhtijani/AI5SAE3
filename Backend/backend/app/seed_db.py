# backend/app/seed_db.py
from .database import SessionLocal, engine, Base
from . import models
from datetime import datetime

def seed():
    # crée les tables si besoin (dev only)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # si la table projects est déjà peuplée, on stoppe
        existing = db.query(models.Project).count()
        if existing > 0:
            print(f"DB already has {existing} project(s). Aborting seed.")
            return

        # exemples de projets statiques
        p1 = models.Project(
            title="Plateforme de réservation de chambres",
            description="Application pour gérer les chambres universitaires.",
            progress=70
        )
        p2 = models.Project(
            title="Analyse Big Data électorale",
            description="Traitement et visualisation de données électorales.",
            progress=50
        )
        p3 = models.Project(
            title="Application mobile de tutorat",
            description="Mise en relation étudiants/tuteurs avec chat et notifications.",
            progress=15
        )
        db.add_all([p1, p2, p3])
        db.commit()

        # refresh pour avoir les id
        db.refresh(p1); db.refresh(p2); db.refresh(p3)

        # activités exemples
        a1 = models.Activity(project_id=p1.id, actor_id=None, action="Initialisation du projet", meta={"note":"seed"}, created_at=datetime.utcnow())
        a2 = models.Activity(project_id=p2.id, actor_id=None, action="Import données", meta={"rows":12000}, created_at=datetime.utcnow())
        db.add_all([a1, a2])
        db.commit()

        # un résumé exemple
        s1 = models.Summary(project_id=p1.id, content="Résumé initial automatique : avancement 70%. Prochaines étapes : finaliser tests.", version=1)
        db.add(s1)
        db.commit()

        print("Seed complete. Created projects:", p1.id, p2.id, p3.id)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
