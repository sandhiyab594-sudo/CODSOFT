

import math
from difflib import get_close_matches


movies = {
    "The Matrix":        {"Action", "Sci-Fi"},
    "Inception":         {"Action", "Sci-Fi", "Thriller"},
    "Interstellar":      {"Sci-Fi", "Adventure", "Drama"},
    "The Avengers":      {"Action", "Sci-Fi", "Adventure"},
    "Titanic":           {"Romance", "Drama"},
    "The Notebook":      {"Romance", "Drama"},
    "La La Land":        {"Romance", "Musical", "Drama"},
    "The Conjuring":     {"Horror", "Thriller"},
    "Get Out":           {"Horror", "Thriller", "Mystery"},
    "Toy Story":         {"Animation", "Adventure", "Comedy"},
    "Finding Nemo":      {"Animation", "Adventure", "Comedy"},
    "The Hangover":      {"Comedy"},
}


ratings = {
    "Alice": {"The Matrix": 5, "The Avengers": 4, "Inception": 5,
              "Interstellar": 5, "Titanic": 2, "The Notebook": 1},
    "Bob":   {"Titanic": 5, "The Notebook": 5, "La La Land": 4,
              "The Matrix": 2, "Inception": 3},
    "Carol": {"The Conjuring": 5, "Get Out": 4, "Inception": 4,
              "The Matrix": 3},
    "Dave":  {"Toy Story": 5, "Finding Nemo": 5, "The Hangover": 4,
              "The Avengers": 3},
    "Eve":   {"La La Land": 5, "Titanic": 4, "The Notebook": 5,
              "Interstellar": 3},
    "Frank": {"The Matrix": 5, "Inception": 5, "The Avengers": 5,
              "Interstellar": 4, "Get Out": 3},
}




def jaccard_similarity(set_a, set_b):
    """0.0 = no genres in common, 1.0 = identical genre sets."""
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union


def recommend_by_content(movie_title, top_n=5):
    target = movies[movie_title]
    scores = []
    for title, genres in movies.items():
        if title == movie_title:
            continue
        sim = jaccard_similarity(target, genres)
        if sim > 0:
            scores.append((title, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]



ALL_MOVIES = list(movies.keys())


def to_vector(user_ratings):
    """Turn {movie: rating} into a fixed-length list, 0 where unrated."""
    return [user_ratings.get(m, 0) for m in ALL_MOVIES]


def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def recommend_by_collaborative(user, top_n=5):
    target_vec = to_vector(ratings[user])
    already_rated = set(ratings[user].keys())

    
    similarities = {}
    for other_user, other_ratings in ratings.items():
        if other_user == user:
            continue
        sim = cosine_similarity(target_vec, to_vector(other_ratings))
        if sim > 0:
            similarities[other_user] = sim

    
    predictions = {}
    for movie in ALL_MOVIES:
        if movie in already_rated:
            continue
        weighted_sum = 0.0
        sim_total = 0.0
        for other_user, sim in similarities.items():
            if movie in ratings[other_user]:
                weighted_sum += sim * ratings[other_user][movie]
                sim_total += sim
        if sim_total > 0:
            predictions[movie] = weighted_sum / sim_total

    ranked = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]



def find_closest(name, options):
    """Case-insensitive exact match, else closest fuzzy match, else None."""
    lower_map = {o.lower(): o for o in options}
    if name.lower() in lower_map:
        return lower_map[name.lower()]
    close = get_close_matches(name, options, n=1, cutoff=0.5)
    return close[0] if close else None


def print_list(title, items):
    print(f"\n{title}:")
    for item in items:
        print(f"  - {item}")


def main():
    print("=" * 60)
    print("   MOVIE RECOMMENDATION SYSTEM")
    print("=" * 60)
    print("Two techniques available:")
    print("  1) Content-based   -> 'movies similar to a movie I liked'")
    print("  2) Collaborative   -> 'movies people like me enjoyed'")

    while True:
        print("\nMenu:")
        print("  1. Recommend by movie (content-based)")
        print("  2. Recommend for a user (collaborative filtering)")
        print("  3. List all movies")
        print("  4. List all users")
        print("  5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            raw = input("Enter a movie you like: ").strip()
            match = find_closest(raw, ALL_MOVIES)
            if not match:
                print(f"Couldn't find a movie matching '{raw}'.")
                print_list("Available movies", ALL_MOVIES)
                continue
            if match.lower() != raw.lower():
                print(f"(Showing results for closest match: '{match}')")
            results = recommend_by_content(match, top_n=5)
            if not results:
                print(f"No similar movies found for '{match}'.")
            else:
                print(f"\nBecause you liked '{match}', you might also like:")
                for title, score in results:
                    print(f"  - {title}  (similarity: {score:.2f})")

        elif choice == "2":
            raw = input("Enter your username: ").strip()
            match = find_closest(raw, list(ratings.keys()))
            if not match:
                print(f"Couldn't find a user matching '{raw}'.")
                print_list("Available users", list(ratings.keys()))
                continue
            if match.lower() != raw.lower():
                print(f"(Showing results for closest match: '{match}')")
            results = recommend_by_collaborative(match, top_n=5)
            if not results:
                print(f"Not enough data to recommend anything new for '{match}'.")
            else:
                print(f"\nUsers similar to '{match}' also enjoyed:")
                for title, score in results:
                    print(f"  - {title}  (predicted rating: {score:.2f}/5)")

        elif choice == "3":
            print_list("All movies", ALL_MOVIES)

        elif choice == "4":
            print_list("All users", list(ratings.keys()))

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()