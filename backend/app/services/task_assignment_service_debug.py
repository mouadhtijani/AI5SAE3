from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util
from ..models import User, Task

# Load model once (global)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

NORMALIZE_MAP = {
    "ml": "machine learning",
    "spring boot": "spring boot",
    "rest api": "rest api",
    "api": "rest api"
}

def normalize_text_list(items: List[str]) -> List[str]:
    normalized = []
    for s in items:
        s_low = s.strip().lower()
        mapped = NORMALIZE_MAP.get(s_low, s_low)
        normalized.append(mapped)
    return normalized

def has_exact_skill(user_skills: List[str], required: List[str]) -> bool:
    if not user_skills or not required:
        return False
    user_set = {s.strip().lower() for s in user_skills}
    for req in required:
        if req.strip().lower() in user_set:
            return True
    return False

def encode_text_list_as_sentence(skills: List[str]) -> str:
    return " ".join(skills) if skills else "no skills specified"

def assign_tasks_debug(users: List[User], tasks: List[Task],
                       alpha: float = 0.5, beta: float = 1.0, exact_boost: float = 1.0) -> Dict[str, Any]:
    debug_results = []

    for task in tasks:
        req_skills_norm = normalize_text_list(task.required_skills)
        task_text = encode_text_list_as_sentence(req_skills_norm)
        task_emb = model.encode(task_text, convert_to_tensor=True)

        best_user_name = None
        best_final_score = -float('inf')
        per_user = []

        for user in users:
            # ✅ Use .skills, .workload — NOT .get()
            user_skills_norm = normalize_text_list(user.skills)
            user_text = encode_text_list_as_sentence(user_skills_norm)
            user_emb = model.encode(user_text, convert_to_tensor=True)

            sim = util.cos_sim(task_emb, user_emb).item()
            exact = has_exact_skill(user.skills, task.required_skills)

            skill_match = sim + (exact_boost if exact else 0.0)
            workload = user.workload  # already a float
            final_score = beta * skill_match - alpha * workload

            per_user.append({
                "name": user.name,
                "role": user.role,
                "original_skills": user.skills,
                "normalized_skills": user_skills_norm,
                "raw_similarity": round(sim, 4),
                "exact_skill_match": exact,
                "skill_match_after_exact_boost": round(skill_match, 4),
                "workload": workload,
                "final_score": round(final_score, 4)
            })

            if final_score > best_final_score:
                best_final_score = final_score
                best_user_name = user.name

        debug_results.append({
            "task": task.title,
            "required_skills": task.required_skills,
            "candidates": per_user,
            "chosen": {
                "name": best_user_name,
                "final_score": round(best_final_score, 4)
            }
        })

    return {"results": debug_results}