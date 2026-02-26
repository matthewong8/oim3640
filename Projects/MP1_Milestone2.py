# Milestone 2: Workout Tracker (Menu + Loop + Validation)

def calculate_volume(sets, reps, weight):
    """Return total training volume for an exercise."""
    return sets * reps * weight


def get_int(prompt, min_value):
    """
    Ask the user for an integer >= min_value.
    Keeps asking until valid.
    """
    while True:
        s = input(prompt)
        try:
            value = int(s)
            if value < min_value:
                print("Please enter a number that is at least", min_value)
            else:
                return value
        except:
            print("Please enter a whole number (example: 3).")


def get_float(prompt, min_value):
    """
    Ask the user for a float >= min_value.
    Keeps asking until valid.
    """
    while True:
        s = input(prompt)
        try:
            value = float(s)
            if value < min_value:
                print("Please enter a number that is at least", min_value)
            else:
                return value
        except:
            print("Please enter a number (example: 25 or 25.5).")


def get_yes_no(prompt):
    """
    Ask user a yes/no question.
    Returns 'y' or 'n'.
    """
    while True:
        ans = input(prompt)
        ans = ans.lower()
        if ans == "y" or ans == "n":
            return ans
        else:
            print("Please type y or n.")


def classify_effort(volume):
    """Describe effort level based on volume."""
    if volume < 4000:
        return "Light"
    elif volume < 8000:
        return "Moderate"
    else:
        return "Intense"


def print_session_summary(total_exercises, total_volume, body_parts):
    print()
    print("----- Session Summary -----")
    print("Exercises logged:", total_exercises)
    print("Total session volume:", total_volume)
    print("Intensity of last workout:", classify_effort(total_volume))
    if total_exercises == 0:
        print("No exercises logged yet.")
        print("Body parts targeted: None")
    else:
        avg = total_volume / total_exercises
        print("Average volume per exercise:", avg)
        # always display body parts line (duplicates removed)
        if body_parts:
            seen = []
            for part in body_parts:
                if part not in seen:
                    seen.append(part)
            print("Body parts targeted:", ", ".join(seen))
        else:
            print("Body parts targeted: None")


def log_one_exercise(target_body_part=None):
    """
    Logs one exercise and returns its volume.
    Also prints a summary for that exercise.  If a target_body_part is
    provided it will be shown in the summary.
    """
    print()
    exercise = input("Exercise name: ")

    sets = get_int("Number of sets: ", 1)
    reps = get_int("Reps per set: ", 1)
    weight = get_float("Weight (lbs, use 0 for bodyweight): ", 0)

    volume = calculate_volume(sets, reps, weight)
    effort = classify_effort(volume)

    print()
    print("--- Exercise Summary ---")
    if target_body_part:
        print("Target body part:", target_body_part)
    print("Exercise:", exercise)
    print("Sets:", sets)
    print("Reps:", reps)
    print("Weight:", weight)
    print("Volume:", volume)
    print("Effort:", effort)

    if weight == 0:
        print("Note: 0 weight entered (bodyweight exercise).")

    return volume


def print_menu():
    print()
    print("=== Workout Tracker Menu ===")
    print("1 - Log an exercise")
    print("2 - View session summary")
    print("3 - Quit")


def main():
    print("Welcome to Workout Tracker (Milestone 2)")
    print("Log exercises and view a running session summary.")

    total_volume = 0.0
    total_exercises = 0
    body_parts = []  # track body parts entered for each exercise

    while True:
        print_menu()
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            target_body_part = input("Target body part: ")
            body_parts.append(target_body_part)
            vol = log_one_exercise(target_body_part)
            total_volume = total_volume + vol
            total_exercises = total_exercises + 1

        elif choice == "2":
            print_session_summary(total_exercises, total_volume, body_parts)

        elif choice == "3":
            print()
            print("See you tomorrow! Nice work today.")
            break

        else:
            print("Please choose 1, 2, or 3.")


main()