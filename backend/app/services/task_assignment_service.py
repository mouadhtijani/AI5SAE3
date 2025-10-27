from sentence_transformers import SentenceTransformer, util

# Load pre-trained model Hugging Face
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def assign_tasks(users, tasks):
    """
    Assign tasks automatically based on skills similarity and workload.
    """
    suggestions = []

    for task in tasks:
        task_skills = " ".join(task.required_skills)
        task_embedding = model.encode(task_skills, convert_to_tensor=True)

        best_user = None
        best_score = -1

        for user in users:
            user_skills = " ".join(user.skills)
            user_embedding = model.encode(user_skills, convert_to_tensor=True)

            similarity = util.cos_sim(task_embedding, user_embedding).item()
            adjusted_score = similarity * (1 - user.workload)  # penalize workload

            if adjusted_score > best_score:
                best_score = adjusted_score
                best_user = user.name

        suggestions.append({
            "task": task.title,
            "assigned_to": best_user,
            "score": round(best_score, 2)
        })

    return suggestions
