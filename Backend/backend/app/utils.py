from fastapi import HTTPException

def not_found(detail="Not found"):
    raise HTTPException(status_code=404, detail=detail)
