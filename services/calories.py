def calculate_calories(
    age,
    height,
    weight,
    activity
):

    bmr = (
        10 * weight
        + 6.25 * height
        - 5 * age
        + 5
    )

    return int(bmr * activity)