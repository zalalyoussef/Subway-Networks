import sys


import tkinter as tk
from tkinter import ttk

#the declared variables are the following:
edges_of_the_graph = []  # List edges of the graph

nodes_choices = []  # List for the dropdown menu for display

node_connections = {}  #stop pairs and corresponding travel time

node_infos = {}  # Dictionary containing the station information

menu_group = {}  # Dictionary for duplicates

nodes = [str(j) for j in range(117)]  # the sist of all stops

Data_File_Path = './Lyon-Data.txt'

visited_nodes = []  # List of visited points to check the connectivity between em

sys.setrecursionlimit(1000)  # Extending number of recursions for the purpose of connectivity checking
#Reading the data of the stations(nodes)from the data text file along with their connections
#and storing them in data structure
#in a way to construct a connected graph 
with open('./Lyon-Data.txt', encoding='utf8') as reader:
    for j in range(117):

        data = reader.readline()
        if j >= 0:

            data = data.split('/')
            chars = '\n'

            data[4] = ''.join( y for y in data[4] if y not in chars)

            node_infos[data[1]]= [data[2],data[3],data[4]]
    for j in range(125):


        data = reader.readline()
        data = data.split(' ')
        chars = '\n'

        data[3] = ''.join(y for y in data[3] if  y not in chars)
        if data[1] in node_connections:

            s = node_connections[data[1]]
            s.extend([data[2], int(data[3])])
            node_connections[data[1]] = s
        else:

            node_connections[data[1]] = [ data[2], int(data[3])]


with open('./Lyon-Data.txt','r') as reader:
        for j in range(117):
           data = reader.readline()
        for j in range(125):
                data = reader.readline()
                data = data.split(' ')
                chars = '\n'

                data[3] = ''.join( y for y  in data[3] if y not in  chars)

                edges_of_the_graph.append((data[1],data[2]))

#creating the adjacency list to represnt the graph
#the return is  a dictionary where a key is a stop and the corresponding value is a list of adjacent stops.
def adjacency():

    adjacency_list_stops = {}
    for Edge in edges_of_the_graph:
        stop1, stop2 = Edge[0], Edge[1]
        if not stop1 in adjacency_list_stops.keys():

            adjacency_list_stops[stop1] = []

        adjacency_list_stops[stop1].append(stop2) 
        if not stop2 in adjacency_list_stops.keys():

            adjacency_list_stops[stop2] = []

        adjacency_list_stops[stop2].append(stop1)
    return adjacency_list_stops

#Ensureing that the edges in the node_connections dic are bidirectional.
# Cheking by: if each stop is connected in both directions and updating the dict to reflect it.
def Both_Directions():

    global node_connections
    for node in nodes:
        if node not in node_connections:
            temporary = []
            for edge in node_connections:
                pair = []
                for j in range(len(node_connections[edge]) // 2):
                    d = (node_connections[edge][j*2], node_connections[edge][(j*2) + 1])
                    pair.append(d)
                for information in pair:
                    if node in information:
                        if node not in temporary:
                            lst = [node, edge, information[1]]
                            temporary.extend(lst)
                        elif node in temporary: 
                            lst = edge, information[1]
                            temporary.extend(lst)
            if temporary != []:

                a1 = temporary.pop(0)
                node_connections[a1] = temporary
    for key in node_connections:

        pair = []

        for j in range(len(node_connections[key]) // 2):
            d = (node_connections[key][j*2], node_connections[key][(j*2) + 1])
            pair.append(d)
            for ok in pair:

                if key not in node_connections[ok[0]]:
                    lst = key, ok[1]
                    node_connections[ok[0]].extend(lst)
Both_Directions()


#returning the route of a given stop including the stop
#numbers and the line numb. It starts with a stop, 
#determines its line numb, and then finds all the stops belonging to the line.
def line(i):

    number = node_infos[i][1]
    last_station = node_infos[i][2].split(',')
    line = [i for i in node_infos if node_infos[i][0] == last_station[0] and node_infos[i][1] == number]
    adj_list = []
    tmporary = []
    for node in line:
        node = str(int(node))
        for j in range(len(node_connections[node]) // 2):
            adj_list.append(node_connections[node][j*2])
            for stop in adj_list:
                new_s = stop
                add = stop
                while len(new_s) != 4:
                    new_s = '0' + add
                    add = new_s
                if node_infos[new_s][1] == number:
                    if new_s not in tmporary:
                        tmporary.append(new_s)
        for j in tmporary:
            if j not in line:
                line.append(j)
    
    return line, number



#this is a recursive fun to check the connectivity of stops in the graph.
# It begins with the given stop from the user and explores all reachable stops, marking them as visited.
def connection(station_depart,adjacency_list_stops):
    global nodes, visited_nodes

    if station_depart not in visited_nodes :

        visited_nodes.append(station_depart)
    for j in adjacency_list_stops[station_depart]:
        if j not in visited_nodes:

            connection(j,adjacency_list_stops)


#Dijkstra_algo function calculates for the shortest way between two stops. 
#returning the shortest one and the time.
def Dijkstra_algo(Departion,arriving):
    Departion = str(int(Departion))
    arriving = str(int(arriving))
    final_dist = {}  
    predecessors = {}  
    tentative_dis = {}
    tentative_dis[Departion] = 0
    visited_stops = [Departion]
    for node in visited_stops:
        final_dist[node] = tentative_dis[node]
        if node == arriving:
            break
        adja_DICT = {}

        for j in range(len(node_connections[node]) // 2):
            adja_DICT[node_connections[node][j*2]] = node_connections[node][(j*2) + 1]
            
        for stop in adja_DICT:
            if stop in visited_stops:
                pass
            if stop not in visited_stops:
                visited_stops.append(stop)
            distance = tentative_dis[node] + int(adja_DICT[stop])
            if stop not in tentative_dis.keys() or distance < tentative_dis[stop]:
                tentative_dis[stop] = distance
                predecessors[stop] = node


    retrieved_path_list = retrieve_path(predecessors,Departion,arriving)
    time = Trip_time(final_dist[arriving])
    return time, retrieved_path_list

# reconstructing the path from the predecessor dict from the Dijkstra algorithm. 
#It retrieves the path from the start stop to the end stop.
def retrieve_path(bb, Departion, arriving):

    retrieved_path_list = [arriving]

    while arriving in bb and bb[arriving] != Departion:
        retrieved_path_list.append(bb[arriving])
        arriving = bb[arriving]

    retrieved_path_list.append(Departion)

    retrieved_path_list.reverse()

    return retrieved_path_list

#processes a list of station IDs, ensuringan ID is 4 chars long,
# and also calculates properties lengths and proximities of certain paths.
# It returns the updated path list along with the length and the proximities.
def Shortest_Dijk_ALGO(c):
    for jj in range(len(c)):
        while len(c[jj]) != 4:
            c[jj] = '0' + c[jj]
    
    dict_longs = {}       
    retrieved_path_list = []  
    proxs = {}   
    
    while c != []:
        if len(c) == 1:
            retrieved_path_list.append(c[0])
            dict_longs[node_infos[c[0]][1]] = 0
            proxs[node_infos[c[0]][1]] = 'Noneeee'
            c.remove(c[0])
        elif len(c) != 1:
            c_list = [station for station in c if node_infos[station][1] == node_infos[c[0]][1]]
            retrieved_path_list.append(c[0])
            retrieved_path_list.append(c[len(c_list)-1]) 
            dict_longs[node_infos[c[0]][1]] = len(c_list) - 1
            proxs[node_infos[c[0]][1]] = c[1]
            c = c[len(c_list):len(c)]
    
    return retrieved_path_list, dict_longs


#handles the cases: a station has many numbers,
#in applying the Dijk algo for each combination of departure and arrival stops to find the shortest one.
def intermediate_paths(Departion, arriving):


    lst_c = [] 

    if len(Departion) == 1 and len(arriving) == 1:
        Departion = Departion[0]
        arriving = arriving[0]
        time, Data_File_Path = Dijkstra_algo(Departion, arriving)
        Data_File_Path = (Data_File_Path,time)
        lst_c.append(Data_File_Path)

    else:
        if len(Departion) > 1 and len(arriving) > 1:
            for stop2 in Departion:
                for stop1 in arriving:
                    time, Data_File_Path = Dijkstra_algo(stop2, stop1)
                    Data_File_Path = (Data_File_Path,time)
                    lst_c.append(Data_File_Path)
        elif len(arriving) > 1:
            
            Departion = Departion[0]
            for stop1 in arriving:

                time, Data_File_Path = Dijkstra_algo(Departion, stop1)
                Data_File_Path = (Data_File_Path,time)
                lst_c.append(Data_File_Path)
        elif len(Departion) > 1:
            arriving = arriving[0]
            for stop2 in Departion:
                time, Data_File_Path = Dijkstra_algo(stop2, arriving)
                Data_File_Path = (Data_File_Path,time)
                lst_c.append(Data_File_Path)
    minimium=lst_c[0]
    for var in lst_c:
        if len(var[0])<len(minimium[0]):
            minimium = var
    time = minimium[1]
    x1,x2 = Shortest_Dijk_ALGO(minimium[0])
    x4 = time
    display_route_info(x1,x2,x4)
    return time


def Trip_time(p):
    if p < 3600:
        min = p//60
        sec = p%60
        time = f'{min} min et {sec} sec.'


    else:
        hr = p//60
        min = p//360
        sec = p%360
        time = f'{hr} hr and {min} min {sec} sec.'
    return time
#displaying the  route info in a UI. 
#It processes the shortest path between stations, line information, and outputs the instructions for the user :)
def display_route_info(route, line_len, end):

    count = 0
    for j in range(len(route)):
        while len(route[j]) != 4:
            route[j] = '0' + route[j]
    
    for j in range(len(route)):
        while len(route[j]) != 4:
            route[j] = '0' + route[j]
        if j != (len(route) - 1):
            while len(route[j + count]) != 4:
                route[j + count] = '0' + route[j + count]
                if len(route[j + count]) == 4:
                    count += 1
        
        m_list, number = line(route[j])
        for d in range(len(m_list)):
            last_station = len(m_list) - 1
            if j == len(route) - 1:
                return end
            if route[j] == m_list[d]:

                if node_infos[route[j]][1] == node_infos[route[j + 1]][1]:
                    var11 = line_len[node_infos[route[j]][1]]
                    if d + var11 < len(m_list):

                        if route[j + 1] == m_list[d + var11]:
                            
                            last_station = m_list[last_station]
                        else:
                            last_station = m_list[0]
                    if d + var11 > len(m_list):

                        if route[j + 1] == m_list[d - var11]:
                            last_station = m_list[0]
                        else:
                            last_station = m_list[last_station]
                    if j == 0:

                        text_box.insert("end", "Take the line: " + str(number) + ", direction to: " + str(
                            node_infos[last_station][0]) + " until you reach " + str(node_infos[route[j + 1]][0]) + ".\n")
                    elif node_infos[route[j]][0] == node_infos[route[j + 1]][0]:

                        text_box.insert("end", "change the line to " + str(node_infos[route[j]][0]) + ".\n")
                    else:

                        text_box.insert("end", "change and take the line: " + str(number) + ", direction to: " + str(
                            node_infos[last_station][0]) + " until you reach: " + str(node_infos[route[j + 1]][0]) + ".\n")
        

"""
    Generating  a menu of stops grouped by their identification name
    and returning
    list: List of station names for the menu.
    Dictionary: Dictionary grouping station IDs by their namessss.
    """
def generate_station_menu():
    global node_infos, menu_group
    for nn in node_infos:
        if node_infos[nn][0] not in menu_group:
            menu_group[node_infos[nn][0]] = [nn]
        else:

            menu_group[node_infos[nn][0]].append(nn)
    for i in menu_group:

        nodes_choices.append(i)

    return nodes_choices, menu_group


generate_station_menu()


def connecting_the_stations(startS,endS):
    """
    Connects the startand end stationsss, finds the shortest path and display it to the user

    Parameters:
    start_station: The starting station name selected by the user
    end_station: The ending station name selected by the user
    """
    if startS == endS :
        text_box.insert("end", "You are already in the station")
    else :
        text_box.insert("end", "You are at: " + str(startS) + ".\n")


        for varrr in menu_group:
            if varrr == startS:
                    start_id=menu_group[varrr]
            if varrr == endS:
                    end_id=menu_group[varrr]
        recup = intermediate_paths(start_id, end_id)
        text_box.insert("end", "You have safely arrived to: " + str(endS) + "!\n")




def press():
    gui.geometry("900x500")
    gui.minsize(400, 400)
    text_box.pack()
    text_box.delete("1.0","end")
    bts['text']="Another Route?"
    depart_point['text']="Select your current station:"
    arrive_pnt['text'] = "Select the destination station:"
    Departure = depart.get()
    Arrival = arrivee.get()
    connecting_the_stations(Departure,Arrival)


gui = tk.Tk()
gui.title("Metro - Lyon")
gui.geometry("900x500")
gui.minsize(400, 200)
gui.config(bg="black")
text_box = tk.Text(gui,bd=0, bg="black", fg="white", font=("Century", 14, 'normal'))
depart_point = tk.Label(gui,fg="white", bg="black", font=("Century",12,'normal'), text="Departing Station")
depart_point.pack(pady=5)
depart = ttk.Combobox(gui, font=("Century",12,'normal'), values=nodes_choices)
depart.current(0)
depart.pack()
arrive_pnt = tk.Label(gui, fg="white", bg="black", font=("Century Gothic",12,'normal'), text="Arriving Station")
arrive_pnt.pack(pady=5)
arrivee = ttk.Combobox(gui, font=("Century",12,'normal'), values=nodes_choices)
arrivee.current(0)
arrivee.pack()
bts = tk.Button(gui, font=("Century",12,'normal'),bg="black",fg="white", text="Find the shortest route", bd='8', command = lambda : press())
bts.pack(pady = 20)
gui.mainloop()