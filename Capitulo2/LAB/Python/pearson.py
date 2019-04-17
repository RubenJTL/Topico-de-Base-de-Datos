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

def PearsonCorrelation(rating1,rating2):
    sumxy=0
    sumx=0
    sumy=0
    sumx2=0
    sumy2=0
    n=0
    for key in rating1:
        if key in rating2:
            n+=1
            x = rating1[key]
            y = rating2[key]
            sumxy+=(x*y)
            sumx+=x
            sumy+=y
            sumx2+=pow(x,2)
            sumy2+=pow(y,2)

    denominator = sqrt(sumx2 - pow(sumx, 2) / n) * sqrt(sumy2 - pow(sumy, 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sumxy - (sumx * sumy) / n) / denominator

def computeNearestNeighbor(username, users):
    distances = []
    for user in users:
        if user != username:
            distance=PearsonCorrelation(users[user], users[username])
            #if (typeDist==1):
            #    distance = ManhattanDistance(users[user], users[username])
            #elif (typeDist==2):
            #    distance = EuclideanDistance(users[user], users[username])
            distances.append((distance, user))
    distances.sort(reverse=True)
    #print(distances)
    return distances

def recommend(username, users):
    nearest = computeNearestNeighbor(username, users)[0][1]
    #print(nearest)
    recommendations = []
    neighborRatings = users[nearest]
    userRatings = users[username]
    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)

print( recommend('Hailey', users))
#print(computeNearestNeighbor("Angelica",users))
#print(PearsonCorrelation(users["Angelica"],users["Bill"]))
