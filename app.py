# MusicApp - Core Application File

def greet_user(name):
    """
    This function greets the user with a personalized message.
    """
    return f"Hello, {name}! Welcome to MusicApp."

def explore_shape_notes():
    """
    Introduces the user to basic shape note solfège using the 7-note system.
    """
    # The 7-note solfège system
    shape_notes_syllables = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Ti"]

    print("\n--- Shape Note Primer ---")
    print("In shape note singing, notes are often sung using solfège syllables.")
    print("We'll focus on the 7-note system, which uses: Do, Re, Mi, Fa, Sol, La, Ti.")
    print("\nHere are the 7-note solfège syllables:")
    print(" ".join(shape_notes_syllables)) # Joins the list elements into a single string with spaces

# Main part of the application
if __name__ == "__main__":
    user_name = input("Please enter your name: ")
    print(greet_user(user_name))

    print("\nWould you like to learn about Shape Notes? (yes/no)")
    learn_shapes = input("Enter your choice: ").lower().strip()

    if learn_shapes == "yes":
        explore_shape_notes()
    else:
        print("Okay, maybe another time. We'll focus on hymns soon!")

    print("\nThanks for using MusicApp!")