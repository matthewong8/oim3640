# Milestone 3: Workout Tracker (Expanded)

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


def print_help():
    print()
    print("----- Help -----")
    print("This app logs exercises and calculates training volume.")
    print("Volume = sets * reps * weight")
    print("Enter 0 for weight if it is a bodyweight exercise.")
    print()
    print("Menu options:")
    print("  1 - Log an exercise (includes body part)")
    print("  2 - View session summary (totals, averages, intensity)")
    print("  3 or q - Quit")
    print()


def remove_duplicates_in_order(items):
    """
    Returns a new list with duplicates removed, keeping original order.
    (Used for displaying body parts cleanly.)
    """
    seen = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def print_session_summary(total_exercises, total_volume, body_parts,
                          total_sets, total_reps,
                          best_exercise_name, best_exercise_volume,
                          best_exercise_body_part):
    print()
    print("----- Session Summary -----")
    print("Exercises logged:", total_exercises)
    print("Total session volume:", total_volume)

    # Your original line (kept)
    print("Intensity of last workout:", classify_effort(total_volume))

    if total_exercises == 0:
        print("No exercises logged yet.")
        print("Body parts targeted: None")
    else:
        avg = total_volume / total_exercises
        print("Average volume per exercise:", avg)

        # New stats (added for Milestone 3 polish)
        print("Total sets:", total_sets)
        print("Total reps:", total_reps)

        if total_sets > 0:
            avg_reps_per_set = total_reps / total_sets
            print("Average reps per set:", avg_reps_per_set)

        # Always display body parts line (duplicates removed) - your logic, but cleaned via helper
        if body_parts:
            unique_parts = remove_duplicates_in_order(body_parts)
            print("Body parts targeted:", ", ".join(unique_parts))
        else:
            print("Body parts targeted: None")

        # New: best exercise tracker
        if best_exercise_name != "":
            print()
            print("Best exercise (highest volume):", best_exercise_name)
            print("Best exercise volume:", best_exercise_volume)
            if best_exercise_body_part != "":
                print("Best exercise body part:", best_exercise_body_part)


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

    # Milestone 3: return more info WITHOUT removing your original behavior.
    # We still return volume, but now we also return exercise name, sets, reps.
    return volume, exercise, sets, reps


def print_menu():
    print()
    print("=== Workout Tracker Menu ===")
    print("1 - Log an exercise")
    print("2 - View session summary")
    print("h - Help")
    print("3 - Quit (or q)")


def main():
    print("Welcome to Workout Tracker (Milestone 3)")
    print("Log exercises and view a running session summary.")
    print("Type 'h' for help.")
    print()

    total_volume = 0.0
    total_exercises = 0
    body_parts = []  # track body parts entered for each exercise

    # Milestone 3: additional session tracking
    total_sets = 0
    total_reps = 0

    best_exercise_name = ""
    best_exercise_volume = 0.0
    best_exercise_body_part = ""

    try:
        while True:
            print_menu()
            choice = input("Choose an option (1/2/h/3 or q): ")

            if choice == "1":
                target_body_part = input("Target body part: ")
                body_parts.append(target_body_part)

                # Updated to accept expanded return values
                vol, name, sets, reps = log_one_exercise(target_body_part)

                total_volume = total_volume + vol
                total_exercises = total_exercises + 1

                # Update new totals
                total_sets = total_sets + sets
                total_reps = total_reps + (sets * reps)

                # Update best exercise (highest volume)
                if total_exercises == 1 or vol > best_exercise_volume:
                    best_exercise_volume = vol
                    best_exercise_name = name
                    best_exercise_body_part = target_body_part

            elif choice == "2":
                print_session_summary(total_exercises, total_volume, body_parts,
                                      total_sets, total_reps,
                                      best_exercise_name, best_exercise_volume,
                                      best_exercise_body_part)

            elif choice == "h" or choice == "H":
                print_help()

            elif choice == "3" or choice == "q" or choice == "Q":
                print()
                print("See you tomorrow! Nice work today.")
                break

            else:
                print("Please choose 1, 2, h, 3, or q.")

    except KeyboardInterrupt:
        print()
        print("Exiting... (Ctrl+C)")
        print("See you tomorrow! Nice work today.")


main()