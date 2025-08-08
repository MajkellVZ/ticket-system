import pandas as pd

def generate_text_sample(df: pd.DataFrame, max_rows: int = 20) -> str:
    texts = []
    for _, row in df.head(max_rows).iterrows():
        s = str(row.get("short_description", ""))
        d = str(row.get("description", ""))
        if s or d:
            texts.append(f"[Short] {s}\n[Desc] {d}")
    return "\n\n".join(texts)

def format_main_causes_prompt(df: pd.DataFrame) -> str:
    sample = generate_text_sample(df)
    return (
        "You are an IT support analyst reviewing user-submitted tickets.\n"
        "From the descriptions below, identify the **main causes** or recurring **themes**.\n\n"
        f"{sample}\n\n"
        "List the main causes as bullets:"
    )

def format_suggestion_prompt(causes: list[str]) -> str:
    causes_list = "\n".join([f"- {c}" for c in causes])
    return (
        "Here are common causes found in IT support tickets:\n\n"
        f"{causes_list}\n\n"
        "For each cause above, suggest clear, actionable solutions or preventative steps."
    )