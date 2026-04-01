def create_message(system_prompt, user_prompt):
    if system_prompt is None:
        return [{"role": "user", "content": user_prompt}]

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]