# MP1 Milestone 1: Workout Tracker (Basic Code)
def calculate_volume(sets, reps, weight):
    """Return total training volume for an exercise."""
    volume = sets * reps * weight
    return volume

def main():
    print("Welcome to Workout Tracker")
    print()

    exercise = input("Exercise name: ")

    sets = int(input("Number of sets: "))
    reps = int(input("Reps per set: "))
    weight = float(input("Weight (lbs, use 0 for bodyweight): "))

    volume = calculate_volume(sets, reps, weight)

    print()
    print("--- Workout Summary ---")
    print("Exercise:", exercise)
    print("Sets:", sets)
    print("Reps:", reps)
    print("Weight:", weight)
    print("Total Volume:", volume)

    # Simple conditional logic (Chapter 5)
    if volume < 500:
        print("Light workout.")
    elif volume < 2000:
        print("Moderate workout.")
    else:
        print("Intense workout.")

main()