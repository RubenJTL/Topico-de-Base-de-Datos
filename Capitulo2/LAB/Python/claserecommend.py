import codecs
from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5,
                      "The Strokes": 2.5, "Vampire Weekend": 2.0},

         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5,
                 "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},

         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5,
                  "Slightly Stoopid": 1.0},

         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},

         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},

         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0,
                     "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 4.0},

         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},

         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
        }



class recommender:

    def __init__(self, data, k=1, metric='0', n=5,r=1):

        self.k = k
        self.n = n
        self.r = r
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        self.metric = metric
        if self.metric == '0':
            self.fn = self.pearson
        elif self.metric == '1':
            self.fn = self.ManhattanDistance
        elif self.metric == '2':
            self.fn = self.EuclideanDistance
        elif self.metric == '3':
            self.fn = self.CosineSimilarity
        elif self.metric == '4':
            self.fn = self.Generalization

        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id


    def userRatings(self, id, n):
        print ("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v)
                   for (k, v) in ratings]
        #print (ratings)

        ratings.sort(key=lambda artistTuple: artistTuple[1],
                     reverse = True)

        #print (ratings)
        ratings = ratings[:n]
        #print (ratings)
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))




    def loadBookDB(self, path=''):
        self.data = {}
        i = 0
        f = codecs.open(path + "BX-Book-Ratings.csv", 'r', 'utf8')
        for line in f:
            i += 1
            fields = line.split(';')
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            #print(fields[2].strip().strip('"'))
            rating = int(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[book] = rating
            self.data[user] = currentRatings
        f.close()

        f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
        for line in f:
            i += 1

            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + ' by ' + author
            self.productid2name[isbn] = title
        f.close()

        f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
        for line in f:
            i += 1
            fields = line.split(';')
            userid = fields[0].strip('"')
            location = fields[1].strip('"')
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'
            if age != 'NULL':
                value = location + '  (age: ' + age + ')'
            else:
                value = location
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()
        print(i)


    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def CosineSimilarity(self,rating1,rating2):
        sumx2=0
        sumy2=0
        sumxy=0
        for key in rating1:
            x=rating1[key]
            sumx2+=pow(x,2)
            if key in rating2:
                y=rating2[key]
                sumxy+=x*y
        for key in rating2:
            y=rating2[key]
            sumy2+=pow(y,2)

        print(sumxy)
        cos=sumxy/(sqrt(sumx2)*sqrt(sumy2))
        return cos

    def ManhattanDistance(self, rating1, rating2):
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

    def EuclideanDistance(self, rating1, rating2):
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

    def Generalization(self, rating1, rating2):
        distance=0
        commonRatings= False
        for key in rating1:
            if key in rating2:
                distance += (abs(rating1[key]-rating2[key]))**self.r
                commonRatings=True
        if commonRatings:
            return (distance**(1.0/self.r))
        else:
            return -1

    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],
                                   self.data[instance])
                distances.append((instance, distance))
        if self.metric=='euclidean' or self.metric=='manhattan' or self.metric=='generalization' :
            distances.sort()
        else:
            distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        #print(distances)
        return distances

    def recommend(self, user):
       recommendations = {}

       nearest = self.computeNearestNeighbor(user)

       userRatings = self.data[user]

       totalDistance = 0.0
       for i in range(self.k):
          totalDistance += nearest[i][1]

       for i in range(self.k):

          weight = nearest[i][1] / totalDistance

          name = nearest[i][0]

          neighborRatings = self.data[name]
          for artist in neighborRatings:
             if not artist in userRatings:
                if artist not in recommendations:
                   recommendations[artist] = (neighborRatings[artist]
                                              * weight)
                else:
                   recommendations[artist] = (recommendations[artist]
                                              + neighborRatings[artist]
                                              * weight)
       recommendations = list(recommendations.items())
       recommendations = [(self.convertProductID2name(k), v)
                          for (k, v) in recommendations]

       recommendations.sort(key=lambda artistTuple: artistTuple[1],
                            reverse = True)
       return recommendations[:self.n]
while True:
    print("0)Internal Data\n 1) BooksDB")
    dboption= (raw_input("DB Option -> "))
    if dboption=='exit':
        break
    if dboption=='0':
        while True:
            print("0) Pearson \n 1) Manhattan \n 2) Euclidean \n 3) Cosine \n 4) Generalization \n ")
            metricIn = (raw_input("Metric Option -> "))
            if metricIn=='exit':
                break
            numK=int(raw_input("K -> "))
            numN=int(raw_input("Vecinos -> "))
            if metricIn=='4':
                numr=int(raw_input("Que valor de r usara -> "))
                r = recommender(users,k=numK,metric=metricIn,n=numN,r=numr)

            else:
                r = recommender(users,k=numK,metric=metricIn,n=numN)

            reco=raw_input("A quien recomendar -> ")
            print(r.recommend(reco))
    else:
        r = recommender(users)
        r.loadBookDB()
        while True:
            reco=raw_input("A quien recomendar -> ")
            if reco=="exit":
                break
            print( r.recommend(reco) )#'171118'
            print(r.userRatings(reco, 5) )
