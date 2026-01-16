import movie_storage_sql as storage
import statistics
import random


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


def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def command_add_movie():
    """Asks user for a movie information and adds it to database"""
    movies = storage.list_movies()
    new_movie_name = input("Enter new movie name: ")
    if new_movie_name in movies:
        print(f"Movie {new_movie_name} already exists!")
        return

    storage.add_movie(new_movie_name)


def command_remove_movie(movies):
    """Removes a movie from the database"""
    while True:
        movie_to_delete = input("Enter movie to delete: ")
        if movie_to_delete in movies:
            storage.delete_movie(movie_to_delete)
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


def command_movie_stats(movies):
    """Prints statistics of the movies"""
    ratings = [info["rating"] for info in movies.values()]
    average = statistics.mean(ratings)
    median = statistics.median(ratings)
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"])
    worst = sorted_movies[0]
    best = sorted_movies[-1]
    print(f'Average rating: {average} \n'
          f'Median rating: {median:.2f} \n'
          f'Best Movie: {best[0]}, {best[1]["rating"]} \n'
          f'Worst Movie: {worst[0]}, {worst[1]["rating"]}')


def command_choose_random_movie(movies):
    """Prints a random movie from the database"""
    random_movie = random.choice(list(movies.keys()))
    movie_rating = movies[random_movie]["rating"]
    print(f"Your movie for tonight: {random_movie}, it's rated {movie_rating}")


def command_search_movie(movies):
    """Search for a movie with a keyword"""
    while True:
        word_to_search = input("Enter part of movie name: ")
        found = False

        for movie, infos in movies.items():
            if word_to_search in movie.lower():
                print(f'{movie}({infos["year"]}): {infos["rating"]}')
                found = True

        if found:
            break
        else:
            print(f'There is no movie with "{word_to_search}" in the name. Please try again.')


def command_best_movies(movies):
    """Prints a sorted list of movies from best to worst rating"""
    sorted_best_to_worst = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse = True)
    for movie, infos in sorted_best_to_worst:
        print(f'{movie}({infos["year"]}): {infos["rating"]}')


def command_generate_website(movies):
    """Generates the html code to create a website"""
    movie_cards_html = ""
    for title, info in movies.items():
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

    with open("index_template.html", "r",) as file:
        template_html = file.read()

    full_website_code = template_html.replace("__TEMPLATE_MOVIE_GRID__", movie_cards_html)

    with open("index.html", "w") as file:
        file.write(full_website_code)

    print("Website generated successfully!")


def main():
    """Main function to call everything"""
    print("*-*-*-*-*", "My Movies", "*-*-*-*-*\n")
    while True:
        movies = storage.list_movies()
        choice = menu_of_programm()
        if choice == 1:
            command_list_movies()
        elif choice == 2:
            command_add_movie()
        elif choice == 3:
            command_remove_movie(movies)
        elif choice == 4:
            command_update_movie()
        elif choice == 5:
            command_movie_stats(movies)
        elif choice == 6:
            command_choose_random_movie(movies)
        elif choice == 7:
            command_search_movie(movies)
        elif choice == 8:
            command_best_movies(movies)
        elif choice == 9:
            command_generate_website(movies)
        elif choice == 0:
            print("Bye!")
            break
        print(input("\nPress Enter to continue"))



if __name__ == "__main__":
    main()
