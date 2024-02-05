# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 21:05:21 2024

@author: Kyle Jared Venter
"""

"""
This is code used to answer questions as part of the CSS Project - Option 1: IMDB Data
"""

#Import pandas for the analysis of the .csv file.
import pandas as pd
import matplotlib.pyplot as plt


#Create a data frame with the imported data. 
#An assumption has been made that the file movie_dataset.csv is present in the same folder as this python file.
imdb_df = pd.read_csv("movie_dataset.csv")
#imdb_df.describe()
#imdb_df.info()

"""
First impressions of the data:
    1) Some columns have more than one item ('Genre' and 'Actors')
    2) Data is somehow ranked
    3) Some of the data will need to be cleaned up
"""

#Cleaning up the data
#Revenue will be filled with the mean revenue of all the films. This will prevent statistics such as overall mean from changing.
imdb_df["Revenue (Millions)"].fillna(imdb_df["Revenue (Millions)"].mean(),inplace=True)
#There is no way to approximate metascore, so these will be left blank. A subset of the data with blanks removed will be used where necessary at a later stage.



#Highest rated movie
#Rating is a float and we can apply the sort_values method to it.
rating_max = imdb_df.sort_values(by = ["Rating"],ascending=False).iat[0,1]
print("Highest rated movie : ",rating_max)



#Average revenue of all movies
average_revenue = imdb_df["Revenue (Millions)"].mean()
print("Average revenue of all movies (millions) :",average_revenue)



#Average revenue of movies from 2015 to 2017
#Create a subset of the data with only relevant years
#A quick glance at the data shows that the upper limit for the year is 2016, but comprehensive code is provided.
revenue_mean_15_to_17 = imdb_df[(imdb_df["Year"] >= 2015) & (imdb_df["Year"] <= 2017)]["Revenue (Millions)"].mean()
print("Average revenue of all movies from 2015 to 2017 (millions) :",revenue_mean_15_to_17)



#How many movies released in 2016
number_movies_2016 = imdb_df[imdb_df["Year"] == 2016]["Title"].count()
print("Number of movies released in 2016 : ",number_movies_2016)



#Movies directed by Christopher Nolan
#Number of movies
c_nolan_movie_number = imdb_df[imdb_df["Director"] == "Christopher Nolan"]["Title"].count()
print("Movies directed by C. Nolan : ",c_nolan_movie_number)
#Median rating of movies
c_nolan_movie_rating = imdb_df[imdb_df["Director"] == "Christopher Nolan"]["Rating"].median()
print("Median rating of movies directed by C. Nolan : ",c_nolan_movie_rating)



#Movies with a rating >= 8.0
high_rating_movies = imdb_df[imdb_df["Rating"] >= 8.0]["Title"].count()
print("Movies with a rating of > 8.0 : ",high_rating_movies)



#Year with the highest average rating
high_rating_year = imdb_df.groupby("Year")["Rating"].mean().sort_values(ascending=False).keys()[0]
print("Year with the highest average rating : ",high_rating_year)



#Percentage increase in movies made from 2006 to 2016
year_num = imdb_df.groupby("Year")["Title"].count()
percentage_increase = ((year_num[2016]-year_num[2006])/year_num[2006])*100
print("Percentage increase from 2006 to 2016 : ",percentage_increase)



#Splitting genre and actor columns
genre_columns = ["Genre1","Genre2","Genre3"]
actor_columns = ["Actor1","Actor2","Actor3","Actor4"]

genre_split_df = imdb_df["Genre"].str.split(r", |,", expand=True)
genre_split_df.columns = genre_columns
actor_split_df = imdb_df["Actors"].str.split(r", |,", expand=True)
actor_split_df.columns = actor_columns

imdb_split_df = pd.merge(imdb_df, genre_split_df,how='outer',left_index=True,right_index=True)
imdb_split_df = pd.merge(imdb_split_df, actor_split_df,how='outer',left_index=True,right_index=True)



#Most common actor
actor_num_list = []
i = 0
for item in actor_columns:
    actor_num = imdb_split_df.groupby(item)["Title"].count()
    actor_num_list.append(actor_num)
    
    if i > 0:
        if i == 1:
            actor_num_df = pd.merge(actor_num_list[i-1], actor_num_list[i],how="outer",left_index=True,right_index=True,suffixes=('_%d'%(i-1), '_%d'%(i)))
        else:
            actor_num_df = pd.merge(actor_num_df, actor_num_list[i],how="outer",left_index=True,right_index=True,suffixes=('_%d'%(i-1), '_%d'%(i)))
    
    i = i + 1
    
actor_num_df.fillna(0, inplace=True) 
common_actor = (sum(actor_num_df["Title_%d"%i] for i in range(4))).sort_values(ascending=False).keys()[0]
print("Most common actor : ",common_actor)    



#Unique genres
genre_num_list = []
i = 0
for item in genre_columns:
    genre_num = imdb_split_df.groupby(item)["Title"].count()
    genre_num_list.append(genre_num)
    
    if i > 0:
        if i == 1:
            genre_num_df = pd.merge(genre_num_list[i-1], genre_num_list[i],how="outer",left_index=True,right_index=True,suffixes=('_%d'%(i-1), '_%d'%(i)))
        else:
            genre_num_df = pd.merge(genre_num_df, genre_num_list[i],how="outer",left_index=True,right_index=True,suffixes=('_%d'%(i-1), '_%d'%(i)))
    
    i = i + 1

genre_total = len(genre_num_df.index)
print("Number of unique genres : ",genre_total) 



"""
Insights
--------

There are a number of columns with numerical data that can be used to draw insights from. Some things which could be analyzed include:
    1) Runtime to revenue
    2) Rating to revenue
    3) Runtime to rating
"""



#Histogram and basic statistics for some of the data. 
#Revenue is not included as mean values were substituted in.


#Number of movies by year
#Using year_num database defined previously
plt.bar(year_num.index,year_num.values, color = "orange")
plt.title("Figure 1: Number of movies by year")
plt.xlabel("Year")
plt.ylabel("Number of movies")
plt.show()


#Average rating by year
plt.bar(imdb_df.groupby("Year")["Rating"].mean().index,imdb_df.groupby("Year")["Rating"].mean().values, color = "grey")
plt.title("Figure 2: Average rating of movies by year")
plt.xlabel("Year")
plt.ylabel("Average Rating")
plt.show()


#Average revenue by year
plt.bar(imdb_df.groupby("Year")["Revenue (Millions)"].mean().index,imdb_df.groupby("Year")["Revenue (Millions)"].mean().values, color = "maroon")
plt.title("Figure 3: Average revenue of movies by year")
plt.xlabel("Year")
plt.ylabel("Average Revenue (Millions)")
plt.show()


#Average runtime by year
plt.bar(imdb_df.groupby("Year")["Runtime (Minutes)"].mean().index,imdb_df.groupby("Year")["Runtime (Minutes)"].mean().values, color = "cyan")
plt.title("Figure 4: Average runtime of movies by year")
plt.xlabel("Year")
plt.ylabel("Average Runtime (Minutes)")
plt.show()


#Histogram of runtime
plt.hist(imdb_df["Runtime (Minutes)"],edgecolor="black", color="darkblue")
plt.title("Histogram of runtime")
plt.xlabel("Runtime (Minutes)")
plt.ylabel("Count")
plt.show()

runtime_mean = imdb_df["Runtime (Minutes)"].mean()
print("Average runtime (minutes) , ",runtime_mean)
runtime_sd = imdb_df["Runtime (Minutes)"].std()


#Runtime vs revenue
plt.scatter(imdb_df["Runtime (Minutes)"],imdb_df["Revenue (Millions)"],marker='+',color='red')
plt.title("Figure 5: Runtime vs Revenue")
plt.xlabel("Runtime (Minutes)")
plt.ylabel("Revenue (Millions)")
plt.show()

#No strong correlation
#Movies under ~85 mintues did not earn above median


#Rating vs runtime
plt.scatter(imdb_df["Runtime (Minutes)"],imdb_df["Rating"],marker='o',color='black')
plt.title("Figure 6: Runtime vs Revenue")
plt.xlabel("Runtime (Minutes)")
plt.ylabel("Rating")
plt.show()


#Rating vs revenue
plt.scatter(imdb_df["Rating"],imdb_df["Revenue (Millions)"],marker='*',color='yellow')
plt.title("Figure 7: Rating vs Revenue")
plt.xlabel("Rating")
plt.ylabel("Revenue (Millions)")
plt.show()


#Assorted numerical insights
print("Most common director : ", imdb_df.groupby("Director")["Title"].count().sort_values(ascending=False).keys()[0])
print("Highest revenue director : ",imdb_df.sort_values(by = ["Revenue (Millions)"],ascending=False).iat[0,4])
print("Highest rating director : ",imdb_df.sort_values(by = ["Rating"],ascending=False).iat[0,4])

#Statistics for these three directors
#Ridley Scott
rs_df = imdb_df[imdb_df["Director"] == imdb_df.groupby("Director")["Title"].count().sort_values(ascending=False).keys()[0]]


#JJ Abrams
jj_df = imdb_df[imdb_df["Director"] == imdb_df.sort_values(by = ["Revenue (Millions)"],ascending=False).iat[0,4]]


#Christopher Nolan
cn_df = imdb_df[imdb_df["Director"] == imdb_df.sort_values(by = ["Rating"],ascending=False).iat[0,4]]


#Revenue boxplots
dir_labels = [imdb_df.groupby("Director")["Title"].count().sort_values(ascending=False).keys()[0],imdb_df.sort_values(by = ["Revenue (Millions)"],ascending=False).iat[0,4],imdb_df.sort_values(by = ["Rating"],ascending=False).iat[0,4]]
plt.boxplot([rs_df["Revenue (Millions)"],jj_df["Revenue (Millions)"],cn_df["Revenue (Millions)"]], labels = dir_labels, vert = False)
plt.title("Figure 8: Boxplot of revenue (millions) for assorted directors")
plt.show()


#Rating boxplots
plt.boxplot([rs_df["Rating"],jj_df["Rating"],cn_df["Rating"]], labels = dir_labels, vert = False)
plt.title("Figure 9: Boxplot of rating for assorted directors")
plt.show()