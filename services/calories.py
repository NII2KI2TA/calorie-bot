def calculate_calories(
        gender,
        weight,
        height,
        age,
        activity
):

    if gender == "male":

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    calories = bmr * activity

    return int(calories)