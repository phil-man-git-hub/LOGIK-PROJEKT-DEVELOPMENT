 # batch_group_nodes.py
# v0.0.1
# 2024-12-19

import flame

this_project = flame.projects.current_project

project_name = this_project.name
# print(this_project.name)

project_nickname = this_project.nickname
# print(this_project.nickname)

current_batch = flame.batch
# print(current_batch.name)

#Create Nodes
first_mux_node = flame.batch.create_node("Mux")

first_elbow_node = flame.batch.create_node("Elbow")

second_mux_node = flame.batch.create_node("Mux")

#Arrange Nodes
first_mux_node.pos_x = 0
first_mux_node.pos_y = 0

first_elbow_node.pos_x = first_mux_node.pos_x + 100
first_elbow_node.pos_y = first_mux_node.pos_y + 100

second_mux_node.pos_x = first_mux_node.pos_x + 200
second_mux_node.pos_y = first_mux_node.pos_y + 000

#Connect Nodes
flame.batch.connect_nodes(first_mux_node, "Default", first_elbow_node, "Default")
flame.batch.connect_nodes(first_elbow_node, "Default", second_mux_node, "Default")
