import numpy as np

def generate_study_plan(attendance, hours, prev_score):
    total_hours = 10
    best_split = {
        "Math": round((100 - prev_score) * 0.04 + hours),
        "Science": round((100 - attendance) * 0.05 + hours),
        "English": round((100 - hours) * 0.05 + 1)
    }
    return best_split