# NO IMPORTS ALLOWED!

import json



  

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    '''checks if 2 actors acted together in the same movie
    using the inputted dataset
    '''
    # with open("small.json") as f:
    #     data = json.load(f)

    #iterates through each list of [actor id, actor id, movie id]
    for list1 in data:
        #if both ids are in same list, they acted together
        if actor_id_1 in list1:
            if actor_id_2 in list1:
                return True
    return False



def gen_dict_of_actor_ids(data):
    '''returns dictionary mapping each id of the actors to
    a set of ids of actors they acted with in the same movie
    '''
    #empty dict to add actos to
    dict_actors = {}

    #iterate through all list in data
    for key in data:
        #if actor acted with his/herself, move on to next
        if key[0] == key[1]:
            continue
        #if new actor, set new key and create emepty set as value
        if key[0] not in dict_actors:
            dict_actors.setdefault(key[0], set())
            #add acting pair to set
            dict_actors[key[0]].add(key[1])
        else:
            #if key already in dict, add second actor to values set
            dict_actors[key[0]].add((key[1]))
        #repeat same processes, but reverse order of assignment
        if key[1] not in dict_actors:
            dict_actors.setdefault(key[1], set())
            dict_actors[key[1]].add(key[0])
        else:
            
            dict_actors[key[1]].add((key[0]))
            

    return dict_actors


def bacon_1_layer(data, n):
    '''
    returns set of actors who Bacon has acted w/
    '''
    #create actor dictionary 
    dict_actors = gen_dict_of_actor_ids(data)
    #parent is Bacon's id number
    parent = 4724
    child = set()
    #iterate through actorss who acted w/ Bacon and add to child
    for i in dict_actors[4724]:
        child.add(i)
    return child

    

def next_layer_of_bacon(data, n):

    '''
    takes in integer value for the Bacon number and returns 
    set of actors who are n connections away from Kevin Bacon
    '''

    #if n is so large that it is larger than the amount of actor pairs, then 
    #it is impossible to get from bacon to actors n actors way from bacon
    if n > len(data):
        return set()
    #create dictionary of actors
    dict_actors = gen_dict_of_actor_ids(data)
    

    
    #get Bacon's set of actors who he has acted w/
    next_child = bacon_1_layer(data,n)
  

    #create empty set and add Bacon's id and ids from first levelof Bacon
    big_set = set()
    big_set.add(4724)
    big_set.update(next_child)

    #check to ensure Bacon is in dictionary
    if 4724 not in dict_actors.keys():
        return set()
    #if n=0, then return Bacon
    if n == 0:
        if 4724 in dict_actors.keys():
            return {4724}
            #if n=1, return first level
    if n == 1:
        return next_child

    #otherwise iterate through each parent and create new child n-1 times
    for n in range(n-1):
        parent = next_child
        #reset next child
        next_child = set()
        for id1 in parent:
            for i in dict_actors[id1]:
                #if actor has already been interated through, then the 
                #actor belongs in a swet w/ smaller bacon number, thus do not 
                #add actor to next child
                if i not in big_set:
                    next_child.add(i)
                    big_set.add(i)

    return next_child


def get_actors_with_bacon_number(data, n):
    '''returns set of actor ids with an inputted bacon number
    '''
    ids = next_layer_of_bacon(data, n)
    #actor_names = id_to_actor(data,ids, n)
    return ids

              
  
def id_to_actor(data, ids, n):

    '''takes in set of ids w/ a specific bacon number
    and returns a lisst of actors asscooated w/ the ids
    '''
    with open('resources/names.json') as f:
  
        namedict = json.load(f)

    ids = next_layer_of_bacon(data, n)
    
    listofnames=[]
    for i in ids:
        for x in namedict.keys():
        
            if namedict[x] == i:
                listofnames.append(x)
    return (set(listofnames))
    
def id_to_actor_spec_id(data, ids):
    '''takes in a list or set of ids and returns 
    and returns liat of names associated w/ the ids
    '''
    with open('resources/names.json') as f:
  
        namedict = json.load(f)
    
    listofnames=[]
    for i in ids:
        for x in namedict.keys():
        
            if namedict[x] == i:
                listofnames.append(x)
    return listofnames

def actor_name_to_id(name):
    '''converts a single actor name into 
    an id, returns an integer representing the id
    '''
    with open('resources/names.json') as f:
  
        namedict = json.load(f)
    id1 = namedict[name]
    return id1

 


    



def get_bacon_path(data, actor_id):
    '''returns path as a set from Bacon to actor_id
    '''

    return get_path(data, 4724, actor_id)



def get_path(data, actor_id_1, actor_id_2):

    #create actor dict
    dict_actors = gen_dict_of_actor_ids(data)
    #start and end destination
    start = actor_id_1
    end = actor_id_2
    
    #check if actor 2 already acted with actor 1
    if end in dict_actors[start]:
        return [start,end]
    #check if actor exist
    if end not in dict_actors:
        return None
    if start not in dict_actors:
        return None
    
    #start queue as True
    queue = True
    #intilzie parents
    parent = {start}
    #big set to avoid repition
    big_set = {start}
    to_add = set()
    #empty set to add already seen actors
    checked = set()
    actor_set = set([actor_id_1])
    #dict to map actors
    map_dict = {}
    #iterate until path is deemed impossible or path is found
    while queue:
       

        #end condition, breka out of loop once actor is found
        if end in actor_set:
            queue = False
            break
        #iterate through each actor in the current layer of connections, finding all of their connections
        for a in actor_set:
            #find actors who the current actor has acted w/
            for a2 in dict_actors[a]:
                #ensure no repeat checks
                if a2 not in checked:
                    checked.add(a)
                    checked.add(a2)
                    to_add.add(a2)
                    #map actors 
                    map_dict[a2] = a
        #if current actors in actor set have no neighbors, path is impossible
        #so return None
        if len(to_add) == 0:
            return None      
        #update actor set
        actor_set.update(to_add)
        #reset to add
        to_add = set()




        

    path = find_path(map_dict, actor_id_1, actor_id_2)
    return path

def find_path(map_dict, actor_id_1, actor_id_2):
    '''
    works backwards to find valid  path from actor id 2 to
    starting actor
    returns list of actor ids from actor id 1 to actor id 2
    '''

    #empty path to add actors
    path = []
    #add actor_id 2 to path
    path.append(actor_id_2)
    
    #find next actor id

    curr_id = map_dict[actor_id_2]

    # add actor to path until current actor is the start actor
    #iterate until we get to fist actor
    while curr_id is not actor_id_1:
        path.append(curr_id)
        print(map_dict)
        curr_id = map_dict[curr_id]
        
    #add first actor since was not added in while loop
    path.append(actor_id_1)
    #reverse path since it started w/ the end actor
    path = path[::-1]
    return path

    
def movie_paths(data, actor_id_1, actor_id_2):
    '''returns list of movie names connecting two actors
    '''
    #get valid path
    id_path = get_path(data, actor_id_1, actor_id_2)
    #lsit to run through
    list1 = data 
    #big list to add movie ids
    big_list = []
    #iterate through each actor and the one to the right of it in the path, excluding last actor
    for i in range(len(id_path)-1):
        i2 = i+1
        newlist = []
        #find movie that the two actors acted in
        for list1 in data:
            if id_path[i] in list1:
                if id_path[i2] in list1:
                    newlist.append(list1[2])
                    print("yo", newlist)
        #add movie to big list
        if len(newlist) > 1:
            big_list.append(newlist[0])
        else:
            if len(newlist) > 0:
                big_list.append(newlist[0])
        
    with open('resources/movies.json') as f:
  
        movies_dict = json.load(f)
    #finds the movie asscoayed with the movie id using movie dict
    movies = []
    for b in big_list:
        for k in movies_dict:
            if b == movies_dict[k]:
                movies.append(k)
    return movies






    

# a = next_layer_of_bacon(smalldb, 4)
    # if 226846 in a[47848]:
    #       print('yes')
    # print(g et_actors_with_bacon_number(smalldb,6))





if __name__ == '__main__':
    with open('resources/large.json') as f:
  
        smalldb = json.load(f)


    

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
# print(did_x_and_y_act_together(smalldb, 46866, 1640))

# print(get_actors_with_bacon_number("t.json", 4))
    # get_bacon_n(smalldb,1640)
    # print(get_bacon_path(smalldb,228546))
    print(get_path(smalldb, 4724, 228546))
    # # print(actor_name_to_id("Iva Ilakovac"))
    # print(id_to_actor_spec_id(smalldb,[141453]))
    # a = (gen_dict_of_actor_ids(smalldb))
    # print(a[141452])
    # if 141452 in a[141450]:
    #     print('yes')
    
    # print(get_actors_with_bacon_number(smalldb, 100000000))
#     # print(movie_paths(smalldb, 6944, 1345462))
# print(did_x_and_y_act_together(smalldb, 4724, 558335))

