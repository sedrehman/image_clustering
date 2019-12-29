"""
K-Means Segmentation Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to segment image using k-means clustering.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are allowed to add your own functions if needed.
You should design you algorithm as fast as possible. To avoid repetitve calculation, you are suggested to depict clustering based on statistic histogram [0,255]. 
You will be graded based on the total distortion, e.g., sum of distances, the less the better your clustering is.
"""
#syed rehman
#syedrehm
#50285410

import utils
import numpy as np
import json
import time

def getLebel_and_total_distance(img, centers):
    k = len(centers)
    total_distance = 0
    #output = np.array(img)
    output = []
    # print(len(output), " and " , len(output[0]))

    for x in range(0,len(img)):
        temp_list = []
        for y in range(0,len(img[x])):
            val = img[x][y]
            dist_from_center = 256
            center_of_choise = 0

            for c in range(0, k):
                dist =  np.abs(val - centers[c])
                if dist < dist_from_center:
                    dist_from_center = dist
                    center_of_choise = c

            total_distance += np.abs(val - centers[center_of_choise])
            #output[x][y] = center_of_choise
            temp_list.append(center_of_choise)
        output.append(temp_list)

    return total_distance, output   
        
    

def kmeans(img,k):
    
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    # TODO: implement this function.
    # high is exclusive and low inclusive.
    centers = []
    for i in range(k):
        centers.append(i)
    prev_k = []
    for c in range(0, k):
        val = np.random.randint(low = 0, high= 256)
        if len(prev_k) > 0:
            for i in range(0, len(prev_k)):
                if prev_k[i] == val:
                    val = np.random.randint(low = 0, high= 256)
                    i = 0
        centers[c] = val
    centers.sort()

    cluster = {}
    for i in range(0, 256):
        cluster[i] = []
    for y in range(0, len(img)):
        for x in range(0, len(img[y])):
            value = img[y][x]
            cluster[value].append((x,y))
    
    #~~~~~~~~~~~~~~~center and clusters done ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    sumdistance = 0

    centerMovement = 256
    interation = 1

    # print("number of centers : " , len(centers))
    # print("centers", centers )

    while (centerMovement > 0):
        cm = 0
        #print("iteration # ", interation)
        cluster_distances = [0] * k  #total distance
        number_of_closest_points = [0] * k   # counter

        for key in cluster:     #key represents all the points with same intensity
            numOfVal = len(cluster[key])
            if numOfVal == 0:
                continue
            dist_from_center = 256
            center_of_choise = 0

            for c in range(0, k):
                dist =  np.abs(key - centers[c])
                if dist < dist_from_center:
                    dist_from_center = dist
                    center_of_choise = c

            
            cluster_distances[center_of_choise] += ((key - centers[center_of_choise]) * numOfVal)
            #print(numOfVal, " goes to ", center_of_choise)
            number_of_closest_points[center_of_choise] += numOfVal
            

    
        cluster_distances_avg = [0]*k
        for i in range(0,k):
            
            if cluster_distances[i] == 0:
                cluster_distances_avg[i] = 0
            else:
                cluster_distances_avg[i] = cluster_distances[i] / number_of_closest_points[i]
            
            val_temp = (int)(centers[i] + cluster_distances_avg[i])
            if val_temp > 255:
                val_temp = 255
            if val_temp < 0:
                val_temp = 0
            
            #print("center", i+1 ," was :" , centers[i], " and now :", val_temp)
            movement_temp = val_temp - centers[i]
            centers[i] = val_temp
            cm += np.abs(movement_temp)

        interation += 1
        centerMovement = cm
        #print("center movement: ", centerMovement, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print(centers)
    # wants centers, lebels and sumdistance
    total_distance , labels = getLebel_and_total_distance(img, centers)
    ddd = int(total_distance)
    return centers, labels, ddd
    


def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    # TODO: implement this function.
    for x in range(0, len(labels)):
        for y in range(0, len(labels[x])):
            val = labels[x][y]
            for c in range(0, len(centers)):
                if val == c:
                    new_val = (int)(centers[c])
                    labels[x][y] = new_val
                    
    img = np.array(labels)
    img = img.astype('uint8')
    return img

     
if __name__ == "__main__":
    img = utils.read_image('test.png')
    k = 2  #you can change this k between (2-255)

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')


"""
for key in clusters:     #key represents all the points with same intensity
        numOfVal = len(clusters[key])
        if numOfVal == 0:
            continue
        dist_from_center = 256
        center_of_choise = 0

        for c in range(0, k):
            dist =  np.abs(key - centers[c])
            if dist < dist_from_center:
                dist_from_center = dist
                center_of_choise = c
        
        total_distance[center_of_choise] += ((key - centers[center_of_choise]) * numOfVal)
        #print(center_of_choise)
"""