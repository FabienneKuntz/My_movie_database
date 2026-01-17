from storage import movie_storage_sql as storage
import statistics
import random
from pathlib import Path


def user_menu():
    """Menu to choose or add a user"""
    users = storage.list_users()
    print("Welcome to the Movie App! 🎬\n")
    while True:
        new_user_number = len(users) + 1
        print("Select a user:")
        if users:
            for user_id, first_name in users.items():
                print(f"{user_id}. {first_name}")
        print(f"{new_user_number}. Create new user")

        user_input = input("\nEnter choice: ").strip()

        if user_input == str(new_user_number):
            new_user_id = command_add_user()
            if new_user_id:
                return new_user_id  # direkt neuen Nutzer auswählen
            else:
                continue

        try:
            user_id = int(user_input)
            if user_id in users:
                print(f"\nHello, {users[user_id]}!\n")
                return user_id
            else:
                print("Invalid user ID.\n")
        except ValueError:
            print("Invalid input. Enter a number.\n")


def command_add_user():
    """Function to create and add a new user to database"""
    users = storage.list_users()
    new_user_name = input("Enter your first name: ").strip()
    if new_user_name in users.values():
        print(f"User {new_user_name} already exists!\n")
        return

    storage.add_user(new_user_name)
    users = storage.list_users() #getting updated users
    new_user_id = next(uid for uid, name in users.items() if name == new_user_name)
    return new_user_id


def menu_of_programm():
    """Shows the user all options to choose from"""
    print("Menu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Generate Website")

    choice = input("Enter choice (0-9): ")
    print()
    if not choice.isdigit():
        print("invalid choice")
    else:
        return int(choice)


def command_list_movies(user_id):
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies(user_id)
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def command_add_movie(user_id):
    """Asks user for a movie information and adds it to database"""
    movies = storage.list_movies(user_id)
    new_movie_name = input("Enter new movie name: ")
    if new_movie_name in movies:
        print(f"Movie {new_movie_name} already exists!")
        return

    storage.add_movie(user_id, new_movie_name)


def command_remove_movie(user_id,movies):
    """Removes a movie from the database"""
    while True:
        movie_to_delete = input("Enter movie to delete: ")
        if movie_to_delete in movies:
            storage.delete_movie(user_id, movie_to_delete)
            break


def command_update_movie():
    """Updates the ranking of a movie from the database"""
    while True:
        movie_to_update = input("Enter movie to update (or type 'menu' to return): ")
        if movie_to_update.lower() == "menu":
            break

        new_movie_rating = float(input("Enter new movie rating (0-10): "))
        storage.update_movie(movie_to_update, new_movie_rating)
        break


def command_movie_stats(user_id, movies):
    """Prints statistics of the movies"""
    user_movies = {title: info for title, info in movies.items() if info.get("user_id") == user_id}

    if not user_movies:
        print("No movies found for this user.")
        return

    ratings = [info["rating"] for info in user_movies.values()]
    average = statistics.mean(ratings)
    median = statistics.median(ratings)
    sorted_movies = sorted(user_movies.items(), key=lambda x: x[1]["rating"])
    worst = sorted_movies[0]
    best = sorted_movies[-1]
    print(f'Average rating: {average} \n'
          f'Median rating: {median:.2f} \n'
          f'Best Movie: {best[0]}, {best[1]["rating"]} \n'
          f'Worst Movie: {worst[0]}, {worst[1]["rating"]}')


def command_choose_random_movie(user_id, movies):
    """Prints a random movie from the database"""
    user_movies = {title: info for title, info in movies.items() if info.get("user_id") == user_id}
    random_movie = random.choice(list(user_movies.keys()))
    movie_rating = user_movies[random_movie]["rating"]
    print(f"Your movie for tonight: {random_movie}, it's rated {movie_rating}")


def command_search_movie(user_id, movies):
    """Search for a movie with a keyword"""
    user_movies = {title: info for title, info in movies.items() if info.get("user_id") == user_id}
    while True:
        word_to_search = input("Enter part of movie name: ")
        found = False

        for movie, infos in user_movies.items():
            if word_to_search in movie.lower():
                print(f'{movie}({infos["year"]}): {infos["rating"]}')
                found = True

        if found:
            break
        else:
            print(f'There is no movie with "{word_to_search}" in the name. Please try again.')


def command_best_movies(user_id, movies):
    """Prints a sorted list of movies from best to worst rating"""
    user_movies = {title: info for title, info in movies.items() if info.get("user_id") == user_id}
    sorted_best_to_worst = sorted(user_movies.items(), key=lambda x: x[1]["rating"], reverse = True)
    for movie, infos in sorted_best_to_worst:
        print(f'{movie}({infos["year"]}): {infos["rating"]}')


def command_generate_website(user_id, movies, users):
    """Generates the html code to create a website"""
    user_movies = {title: info for title, info in movies.items() if info.get("user_id") == user_id}

    if not user_movies:
        print("No movies found for this user.")
        return

    movie_cards_html = ""
    for title, info in user_movies.items():
        poster_url = info.get("poster_url")
        movie_cards_html += f"""    <li>
                <div class="movie">
                    <img class="movie-poster"
                         src="{poster_url}"
                         title="{title}"/>
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{info['year']}</div>
                </div>
            </li>\n"""

    project_root = Path(__file__).resolve().parent.parent
    template_path = project_root / "web" / "index_template.html"

    username = users.get(user_id, f"user{user_id}")  # fallback, falls Username nicht gefunden
    output_path = project_root / "web" / f"{username}.html"

    with open(template_path, "r") as file:
        template_html = file.read()

    full_website_code = template_html.replace("__TEMPLATE_MOVIE_GRID__", movie_cards_html)

    with open(output_path, "w") as file:
        file.write(full_website_code)

    print("Website generated successfully!")


def main():
    """Main function to call everything"""
    print("*-*-*-*-*", "My Movies", "*-*-*-*-*\n")
    current_user_id = user_menu()

    while True:
        movies = storage.list_movies(current_user_id)
        choice = menu_of_programm()
        if choice == 1:
            command_list_movies(current_user_id)
        elif choice == 2:
            command_add_movie(current_user_id)
        elif choice == 3:
            command_remove_movie(current_user_id, movies)
        elif choice == 4:
            command_update_movie()
        elif choice == 5:
            command_movie_stats(current_user_id, movies)
        elif choice == 6:
            command_choose_random_movie(current_user_id, movies)
        elif choice == 7:
            command_search_movie(current_user_id, movies)
        elif choice == 8:
            command_best_movies(current_user_id, movies)
        elif choice == 9:
            users = storage.list_users()
            command_generate_website(current_user_id, movies, users)
        elif choice == 0:
            print("Bye!")
            break
        print(input("\nPress Enter to continue"))


if __name__ == "__main__":
    main()
