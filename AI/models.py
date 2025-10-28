from sqlalchemy import Column, Integer, String, Date
from database import Base
from datetime import date

class Rapport(Base):
    __tablename__ = "rapports"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    description = Column(String)
    date_creation = Column(Date, default=date.today)
    auteur = Column(String, nullable=False)
    type_export = Column(String, default="PDF")
