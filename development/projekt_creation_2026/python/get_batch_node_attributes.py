# import flame

# help(flame)
# for I in dir(flame):
#     print(I)

# help(flame.batch)
# for I in dir(flame.batch):
#     print(I)



# import flame

# this_project = flame.project.current_project

# project_name = this_project.name
# print(this_project.name)

# project_nickname = this_project.nickname
# print(this_project.nickname)

# current_batch = flame.batch
# print(current_batch.name)



# import flame
# current_batch = flame.batch

# # Just try to print basic info about nodes
# for node in current_batch.nodes:
#     print(f"Found node: {node.name}")



import flame

# Get current batch
current_batch = flame.batch

# Function to print node attributes
def print_node_attributes(node):
    for attr in node.attributes:
        print(f"Attribute: {attr}")
        try:
            value = getattr(node, attr)
            print(f"Value: {value}\n")
        except Exception as e:
            print(f"Could not get value: {e}\n")

# Get selected nodes
selected_nodes = [node for node in current_batch.nodes if node.selected]

# Print info for selected nodes
for node in selected_nodes:
    print(f"\nNode Name: {node.name}")
    print("=" * 50)
    print_node_attributes(node)