import random
import math
from flask import Flask, render_template
from flask import Flask, request
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import threading



app = Flask(__name__, static_folder='static')

stop_words = set(stopwords.words('english'))



def get_videos():
    with open('5unique_data.json') as f:
        videos = json.load(f)

    with open('5unique_data_ids.json') as f:
        data = json.load(f)
        video_ids = data['video_ids']

    return videos, video_ids

videos, video_ids = get_videos()

def stats(user_activity):

    categories = {}

    for video_id in user_activity:
        index = video_ids.index(video_id)
        video = videos[index]
        category = video['category']
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    print("Categories_user:")
    for category, count in categories.items():
        print(f"{category}: {count} videos")

     # Plot bar chart
    # Plot pie chart
    # Plot pie chart
    categories_sorted = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    colors = plt.cm.Set3.colors[:len(categories_sorted)]
    patches, texts = plt.pie(categories_sorted.values(),  colors=colors, startangle=90)

    # Add legend
    legend_labels = [f"{category}: {count} videos ({count/len(user_activity)*100:.1f}%)" for category, count in categories_sorted.items()]
    plt.legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)

    # Add labels
    plt.title('STATISTICS')
    plt.show()

def stats_result(new_results):
    categories = {}

    for video in new_results:
        category = video['category']
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    print("Categories:")
    for category, count in categories.items():
        print(f"{category}: {count} videos")

    # Plot pie chart
    categories_sorted = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    colors = plt.cm.Set3.colors[:len(categories_sorted)]
    patches, texts = plt.pie(categories_sorted.values(),  colors=colors, startangle=90)

    # Add legend
    legend_labels = [f"{category}: {count} videos ({count/len(new_results)*100:.1f}%)" for category, count in categories_sorted.items()]
    plt.legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)

    # Add labels
    plt.title('STATISTICS')
    plt.show()


try:
    with open('database_user.json', 'r') as f:
        user_activity = json.load(f)
except FileNotFoundError:
    user_activity = []


def get_related_videos(user_activity, videos):
    list_of_user_activity = []
    user_activity = user_activity

    #retrieving videos having similar tags to those from user_activity
    related_videos_tags = []
    for video_id in user_activity:
        for video in videos:
            if video['video_id'] == video_id:
                clicked_video = video
                break
        for video in videos:
            for tag in video['tags']:
                for clicked_tag in clicked_video['tags']:
                    clicked_tag_words = clicked_tag.split()
                    clicked_tag_words = [word for word in clicked_tag_words if word.lower() not in stop_words]
                    if any(clicked_tag_word in tag for clicked_tag_word in clicked_tag_words) and video != clicked_video and video not in related_videos_tags:
                        related_videos_tags.append(video)

    #making a list of video and corresponding category, from list of video_ids from user activity
    for value in user_activity:
        for video in videos:
            if value == video["video_id"]:
                category = video["category"]
                list_of_user_activity.append({"video_id": value, "category" : category})
    # print("list of user activity")
    # print(list_of_user_activity)
    
    #using list_of_user_category for making another list containing category and it's count, from user activity          
    category_likes = {}
    for activity in list_of_user_activity:
        category = activity['category']
        category_likes[category] = category_likes.get(category, 0) + 1
    # print("category likes")
    # print (category_likes)

    #using category_likes to retrive all the videos of categories present in category_likes, list format = ["cat" : [{}{}]]
    videos_by_category = {}
    for video in videos:
        if video['category'] in category_likes:
            if video['category'] not in videos_by_category:
                videos_by_category[video['category']] = []
            videos_by_category[video['category']].append(video)

    # Calculate the proportion of videos to include for each category
    total_likes = sum(category_likes.values())
    category_proportions = {}
    for category, likes in category_likes.items():
        if category in videos_by_category:
            num_videos_in_category = len(videos_by_category[category])
            category_proportions[category] = likes / total_likes * num_videos_in_category / len(videos)

    # print("category prportions")
    # print(category_proportions)

    # Calculate the number of videos to include for each category
    num_videos_per_category = {}
    for category, proportion in category_proportions.items():
        num_videos_per_category[category] = int(proportion * len(videos))
    # print("num videos per category")
    # print(num_videos_per_category)

    # Sort the videos by category and shuffle within each category
    sorted_videos = []
    for category, num_videos in num_videos_per_category.items():
        sorted_videos += random.sample(videos_by_category[category], num_videos)
    random.shuffle(sorted_videos)


    # Add 10% of videos randomly to the final sorted_videos list
    num_random_videos = int(0.1 * len(sorted_videos))
    random_videos = random.sample(videos, num_random_videos)
    sorted_videos += random_videos
    random.shuffle(sorted_videos)

    # Add 10% of videos with related tags to the final sorted_videos list
    num_tag_videos = int(0.1 * len(sorted_videos))
    tag_videos = random.sample(related_videos_tags, num_tag_videos)
    sorted_videos += tag_videos
    random.shuffle(sorted_videos)
    
    # Calculate counts and percentages of categories in user activity
    print("User activity:")
    total_activity = sum(category_likes.values())
    for category, likes in category_likes.items():
        category_percent = likes / total_activity * 100
        print(f"{category}: {likes} likes ({category_percent:.2f}%)")

    # Get the total count of videos
    total_videos = sum(num_videos_per_category.values())

    # Calculate the proportions of videos per category
    category_proportions = {category: num_videos/total_videos for category, num_videos in num_videos_per_category.items()}

    # Add the category_proportions of random videos and tag videos
    category_proportions["Random Videos"] = num_random_videos/total_videos
    category_proportions["Tag Videos"] = num_tag_videos/total_videos
    
    # Plot the pie chart
    labels = category_proportions.keys()
    sizes = category_proportions.values()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    #retrieving data of top 5 videos, using genetic algo and simmulated annealing algo
    top_5 = genetic(sorted_videos)
    sorted_videos_filtered = sorted_videos
    for video in top_5:
        video_id = video["video_id"]
        for element in sorted_videos:
            if video_id == element["video_id"]:
                sorted_videos_filtered.remove(element)
    
    sorted_videos = []
    #concatenating both the variables, keeping top_5 at first so as to display top 5 on top
    sorted_videos = top_5 + sorted_videos_filtered

    return sorted_videos

def simulated_annealing(initial_temperature, cooling_rate, stopping_temperature, solo_id_fitness, initial_population):
    current_solution = initial_population[0]
    current_energy = sum(solo_id_fitness[current_solution.index(y)] for y in current_solution)
    best_solution = current_solution.copy()
    best_energy = current_energy

    temperature = initial_temperature
    while temperature > stopping_temperature:
        for i in range(len(video_ids)):
            neighbor_solution = current_solution.copy()
            gene_index = random.randint(0, 4)
            while True:
                random_choice = random.choice(video_ids)
                if random_choice not in neighbor_solution:
                    break
            neighbor_solution[gene_index] = random_choice
            neighbor_energy = sum(solo_id_fitness[neighbor_solution.index(y)] for y in neighbor_solution)
            delta_energy = neighbor_energy - current_energy
            if delta_energy < 0 or math.exp(-delta_energy / temperature) > random.uniform(0, 1):
                current_solution = neighbor_solution
                current_energy = neighbor_energy
            if current_energy < best_energy:
                best_solution = current_solution
                best_energy = current_energy
        temperature *= cooling_rate

    return best_solution, best_energy

def genetic(sorted_for_gen1):

    sorted_for_gen = sorted_for_gen1

    related_video_ids = []
    for item in sorted_for_gen:
        related_video_ids.append(item["video_id"])


    initial_population = []
    for i in range(100):
        comb_web_ids = random.sample(related_video_ids, 5)
        initial_population.append(comb_web_ids)
    print(initial_population)
    print("\n\n")

    tags_list = [tag for video in videos for tag in video['tags']]

    view_list = []
    like_list = []
    dislike_list = []
    for video in videos:
        view_list.append(int(video['view_count']))
        
        if isinstance(video['like_count'], list):
            like_list.extend([int(like) for like in video['like_count']])
        else:
            like_list.append(int(video['like_count']))
            
        if isinstance(video['dislike_count'], list):
            dislike_list.extend([int(dislike) for dislike in video['dislike_count']])
        else:
            dislike_list.append(int(video['dislike_count']))



    solo_id_fitness = []  #evaluation of all the attributes of each video, using instead of randomkeywords, fucked up document
    for i in range(len(view_list)):
        view = view_list[i]
        like = like_list[i]
        dislike = dislike_list[i]
        like_dislike_ratio = 0
        if dislike == 0:
            like_dislike_ratio = like
        else:
            like_dislike_ratio = like/(dislike*0.1)
        eval = (view*0.6) + (like_dislike_ratio*0.4)
        solo_id_fitness.append(eval)


    # Step 2: Loop for N generations
    for generation in range(1, 101):

        # Step 3: Select the candidates for crossover using binary tournament selection
        crossover_population = []
        for i in range(int(len(initial_population)*0.1)):
            tournament_selection = random.sample(initial_population, 3)
            fittest_web_ids = max(tournament_selection, key=lambda x: sum(solo_id_fitness[x.index(y)] for y in x))
            less_fittest_web_ids = min(tournament_selection, key=lambda x: sum(solo_id_fitness[x.index(y)] for y in x))
            rand_var = random.uniform(0, 1)
            if rand_var < 0.7:  # crossover rate (CR) = 0.7
                crossover_population.append(fittest_web_ids)
            else:
                crossover_population.append(less_fittest_web_ids)
        
        # Step 4: Performing Crossover
        new_population = []
        for i in range(0, 100, 2):
            parent1, parent2 = random.sample(crossover_population, 2)
            crossover_point = random.randint(1, 4)
            offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
            offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
            new_population.append(offspring1)
            new_population.append(offspring2)

        # Step 5: Apply mutation with mutation rate, MR
        for i in range(len(new_population)):
            mutation_probability = 0.01  # mutation rate (MR) = 0.01
            if random.uniform(0, 1) <= mutation_probability:
                gene_index = random.randint(0, 4)
                new_population[i][gene_index] = random.choice(related_video_ids)

        # Step 6: Copy new generation to initial population
        initial_population = new_population

    # Step 9: Return InitialPopulation[0]
    fittest_web_ids = max(initial_population, key=lambda x: sum(solo_id_fitness[x.index(y)] for y in x))
    print(f"best genetic solution: {fittest_web_ids}")
    best_genetic_energy = sum(solo_id_fitness[fittest_web_ids.index(y)] for y in fittest_web_ids)
    print(f"best genetic energy: {best_genetic_energy}")


    web_result_genetic = []
    for value in fittest_web_ids:
        print(value)
        index = video_ids.index(value)
        web_result_genetic.append(videos[index])



    best_simulated_solution, best_simulated_energy = simulated_annealing(100, 0.94, 1, solo_id_fitness, initial_population)
    print(f"Best simulated Solution: {best_simulated_solution}")
    print(f"Best simulated Energy: {best_simulated_energy}")


    web_result_simulated = []
    for value in best_simulated_solution:
        print(value)
        index = video_ids.index(value)
        web_result_simulated.append(videos[index])



    web_result = []
    web_result = web_result_simulated
    return web_result

@app.route('/', methods=['GET', 'POST'])
def index():
    print("index() function called")
    if request.method == 'POST':
        liked_video_id = request.form.get('liked_video_id')
        if liked_video_id and liked_video_id not in user_activity:
            user_activity.append(liked_video_id)
            # Update liked videos file
            with open('database_user.json', 'w') as f:
                json.dump(user_activity, f)
    else:
        if user_activity: #have to send likedvideoid from here to related videos
            print(user_activity)
            stats(user_activity)
            new_results = get_related_videos(user_activity,videos)

            t2 = threading.Thread(target=stats_result, args=(new_results,))
            t2.start()

            return render_template('like.html', videos = new_results)
        else:
            t1 = threading.Thread(target=stats_result, args = (videos,))
            t1.start()
            print(video_ids)
            return render_template('like.html', videos = videos)

if __name__ == '__main__':
    app.run(debug=True)
