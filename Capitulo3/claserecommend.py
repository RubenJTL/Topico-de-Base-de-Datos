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

users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
         "Ben": {"Taylor Swift": 5, "PSY": 2},
         "Clara": {"PSY": 3.5, "Whitney Houston": 4},
         "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
                    "Lorde": 4, "Fall Out Boy": 1},
         "Matt": {"Imagine Dragons": 3, "Daft Punk": 4,
                    "Lorde": 4, "Fall Out Boy": 1},
         "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3,
                    "Lorde": 3, "Fall Out Boy": 1},
         "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
                    "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
         "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4,
                    "Daft Punk": 5, "Fall Out Boy": 3}}

def computeUserAverages(users):
   results = {}
   for (key, ratings) in users.items():
      results[key] = float(sum(ratings.values())) / len(ratings.values())
   return results


def computeSimilarity(band1, band2, userRatings):
    averages = {}
    for (key, ratings) in userRatings.items():
        averages[key] = (float(sum(ratings.values()))/ len(ratings.values()))
    num = 0 # numerator
    denominador1 = 0 # first half of denominator
    denominador2 = 0
    for (user, ratings) in userRatings.items():
        if band1 in ratings and band2 in ratings:
            avg = averages[user]
            num += (ratings[band1] - avg) * (ratings[band2] - avg)
            denominador1 += (ratings[band1] - avg)**2
            denominador2 += (ratings[band2] - avg)**2
    return num / (sqrt(denominador1) * sqrt(denominador2))

class recommender:

    def __init__(self, data, k=1, metric='0', n=5,r=1):

        self.k = k
        self.n = n
        self.r = r
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        self.frequencies = {}
        self.deviations = {}
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

    def showUserTopItems(self, user, n):
      """ show top n items for user"""
      items = list(self.data[user].items())
      items.sort(key=lambda itemTuple: itemTuple[1], reverse=True)
      for i in range(n):
         print("%s\t%i" % (self.convertProductID2name(items[i][0]),
                           items[i][1]))

    def loadMovieLens(self, path=''):
      self.data = {}
      i = 0
      #f = codecs.open(path + "u.data", 'r', 'utf8')
      f = codecs.open(path + "u.data", 'r', 'ascii')
      #  f = open(path + "u.data")
      for line in f:
         i += 1
         fields = line.split('\t')
         user = fields[0]
         movie = fields[1]
         rating = int(fields[2].strip().strip('"'))
         if user in self.data:
            currentRatings = self.data[user]
         else:
            currentRatings = {}
         currentRatings[movie] = rating
         self.data[user] = currentRatings
      f.close()
      #f = codecs.open(path + "u.item", 'r', 'utf8')
      f = codecs.open(path + "u.item", 'r', 'iso8859-1', 'ignore')
      #f = open(path + "u.item")
      for line in f:
         i += 1
         fields = line.split('|')
         mid = fields[0].strip()
         title = fields[1].strip()
         self.productid2name[mid] = title
      f.close()
      #f = codecs.open(path + "u.user", 'r', 'utf8')
      f = open(path + "u.user")
      for line in f:
         i += 1
         fields = line.split('|')
         userid = fields[0].strip('"')
         self.userid2name[userid] = line
         self.username2id[line] = userid
      f.close()
      print(i)

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

    def computeDeviations(self):

      for ratings in self.data.values():
         for (item, rating) in ratings.items():
            self.frequencies.setdefault(item, {})
            self.deviations.setdefault(item, {})
            for (item2, rating2) in ratings.items():
               if item != item2:
                  self.frequencies[item].setdefault(item2, 0)
                  self.deviations[item].setdefault(item2, 0.0)
                  self.frequencies[item][item2] += 1
                  self.deviations[item][item2] += rating - rating2

      for (item, ratings) in self.deviations.items():
         for item2 in ratings:
            ratings[item2] /= self.frequencies[item][item2]

    def slopeOneRecommendations(self, userRatings):
      recommendations = {}
      frequencies = {}
      for (userItem, userRating) in userRatings.items():
         for (diffItem, diffRatings) in self.deviations.items():
            if diffItem not in userRatings and \
               userItem in self.deviations[diffItem]:
               freq = self.frequencies[diffItem][userItem]
               recommendations.setdefault(diffItem, 0.0)
               frequencies.setdefault(diffItem, 0)
               recommendations[diffItem] += (diffRatings[userItem] +
                                             userRating) * freq
               frequencies[diffItem] += freq
      recommendations =  [(self.convertProductID2name(k),
                           v / frequencies[k])
                          for (k, v) in recommendations.items()]
      recommendations.sort(key=lambda artistTuple: artistTuple[1],
                           reverse = True)
      return recommendations[:50]

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
    print("0)Internal Data\n1)BooksDB\n2)MovieLens")
    dboption= (raw_input("DB Option -> "))
    if dboption=='exit':
        break
    if dboption=='0':
        while True:
            print("0)User1\n1)User2\n2)User3")
            useroption=(raw_input("DB Option -> "))
            if useroption=='0':
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
            elif useroption=='1':
                 r = recommender(users2)
                 print(r.computeDeviations())
                 g = users2['Ben']
                 print(r.slopeOneRecommendations(g))
            elif useroption=='2':
                bands = ['Kacey Musgraves', 'Daft Punk', 'Imagine Dragons', 'Lorde', 'Fall Out Boy']
                for b in bands:
                   for x in bands:
                      print("%20s%20s%10.5f" % (b, x, computeSimilarity(b, x, users3)))
                print (computeUserAverages(users3))


    elif dboption=='1':
        r = recommender(users)
        r.loadBookDB()
        while True:
            reco=raw_input("A quien recomendar -> ")
            if reco=="exit":
                break
            print( r.recommend(reco) )#'171118'
            print(r.userRatings(reco, 5) )

    elif dboption=='2':
        r = recommender(0)
        r.loadMovieLens('ml-100k/')

        while True:
            reco=raw_input("A quien recomendar -> ")
            if reco=="exit":
                break
            #r.showUserTopItems('1', 50)
            r.computeDeviations()
            print(r.slopeOneRecommendations(r.data['1']))
            print(r.slopeOneRecommendations(r.data['25']))
            #print( r.recommend(reco) )#'171118'
            #print(r.userRatings(reco, 5) )
