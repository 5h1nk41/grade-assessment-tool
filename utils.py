import openai

openai.api_key = "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"

def generate_self_evaluation(achievement_points, model="text-davinci-003"):
    prompt = f"実績の要点: {achievement_points}\n自己評価: "
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.1
    )

    return response.choices[0].text.strip()

def check_requirements(achievement_points, grade, grade_requirements):
    requirements_met = []

    for requirement in grade_requirements[grade]:
        if requirement in achievement_points:
            requirements_met.append(True)
        else:
            requirements_met.append(False)

    return all(requirements_met)
