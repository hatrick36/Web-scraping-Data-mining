import csv
import numpy
import os
# takes data written to csv by insta_follow.py and opens it 
with open('follow.csv', 'r') as csv_file:
    lines = csv_file.readlines()
following = []
followers = []
# appends data do lists
for line in lines:
    data = line.split(',')
    following.append(data[1])
    followers.append(data[2])
print(following)
print(followers)
# shows user what followers are not following them back
not_following_back = [user for user in following if user not in followers]
not_following_back = [i for i in not_following_back if i]
print(not_following_back)
print(len(not_following_back))
print('It appears', len(not_following_back), 'users are not following you back')






