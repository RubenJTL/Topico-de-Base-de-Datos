from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

def ManhattanDistance(rating1, rating2):
    distance=0
    commonRatings = False
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            commonRatings = True
    if commonRatings:
        return distance
    else:
        return -1

def EuclideanDistance(rating1, rating2):
    distance=0
    commonRatings = False
    for key in rating1:
        if key in rating2:
            distance += (rating1[key] - rating2[key])**2
            commonRatings = True
    if commonRatings:
        return (sqrt(distance))
    else:
        return -1

def Generalization(rating1, rating2, r):
    distance=0
    commonRatings= False
    for key in rating1:
        if key in rating2:
            distance += (abs(rating1[key]-rating2[key]))**r
            commonRatings=True
    if commonRatings:
        return (distance**(1.0/r))
    else:
        return -1

def computeNearestNeighbor(username, users, typeDist):
    distances = []
    for user in users:
        if user != username:
            distance=Generalization(users[user], users[username],typeDist)
            #if (typeDist==1):
            #    distance = ManhattanDistance(users[user], users[username])
            #elif (typeDist==2):
            #    distance = EuclideanDistance(users[user], users[username])
            distances.append((distance, user))
    # sort based on distance -- closest first
    distances.sort()
    return distances

def recommend(username, users,typeDist):
    nearest = computeNearestNeighbor(username, users,typeDist)[0][1]
    print(nearest)
    recommendations = []
    neighborRatings = users[nearest]
    userRatings = users[username]
    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)


print( recommend('Hailey', users,2))
#print(Generalization(users["Hailey"],users["Veronica"],1))
#print( computeNearestNeighbor("Hailey", users,2))
