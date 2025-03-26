# DeNoise_Pipeline.py
# v0.0.1
# 2025-01-19

import flame

this_project = flame.project.current_project

project_name = this_project.name
print(this_project.name)

project_nickname = this_project.nickname
print(this_project.nickname)

current_batch = flame.batch
print(current_batch.name)

current = flame.batch.current_node.get_value()

original_clip = flame.batch.create_node("Mux")

denoise_compass = flame.batch.create_node("Compass")

match_grain_compass = flame.batch.create_node("Compass")

color_mgnt_1 = flame.batch.create_node("Colour Mgmt")

ofx_1 = flame.batch.create_node("OpenFX")

color_mgnt_2 = flame.batch.create_node("Colour Mgmt")

write_denoise = flame.batch.create_node("Write File")

degrained_clip = flame.batch.create_node("Mux")

pre_comp = flame.batch.create_node("Mux")

match_grain = flame.batch.create_node("Match Grain")

original_clip.name = 'Original_Clip'
original_clip.collapsed = True
original_clip.pos_x = 0
original_clip.pos_y = 0

denoise_compass.name = 'DeNoise_Pipeline'
denoise_compass.pos_x = original_clip.pos_x - 200
denoise_compass.pos_y = original_clip.pos_y - 200
denoise_compass.height = 800
denoise_compass.width = 1600
denoise_compass.colour = (0.0,0.194,0.0)

color_mgnt_1.name = 'AP1_to_Rec709_32Bit'
color_mgnt_1.pos_x = original_clip.pos_x + 200
color_mgnt_1.pos_y = original_clip.pos_y + 200

ofx_1.change_plugin("Reduce_Noise_v5")
ofx_1.name = 'NEAT_Reduce_Noise'
ofx_1.collapsed = True
ofx_1.pos_x = color_mgnt_1.pos_x + 200
ofx_1.pos_y = color_mgnt_1.pos_y + 200

# ofx_2.change_plugin("Mocha Pro")
# ofx_2.name = 'Mocha_Pro'
# ofx_2.collapsed = True
# ofx_2.pos_x = color_mgnt_1.pos_x + 200
# ofx_2.pos_y = color_mgnt_1.pos_y + 200

# ofx_3.change_plugin("Silhouette")
# ofx_3.name = 'Silhouette'
# ofx_3.collapsed = True
# ofx_3.pos_x = color_mgnt_1.pos_x + 200
# ofx_3.pos_y = color_mgnt_1.pos_y + 200

color_mgnt_2.name = 'Rec709_to_AP1'
color_mgnt_2.pos_x = ofx_1.pos_x + 200
color_mgnt_2.pos_y = ofx_1.pos_y - 200

write_denoise.name = 'Write_DeNoise'
# write.name = '<batch name>_deNoise_pre<iteration##>'
write_denoise.pos_x = color_mgnt_2.pos_x + 400
write_denoise.pos_y = color_mgnt_2.pos_y + 200
write_denoise.bypass = False
write_denoise.schematic_colour = (0.6, 0.0, 0.0)
    # write.destination = ('Batch Reels', 'neat_video')
    # write.media_path = write_path
    # write.media_path_pattern = "<name>"
    # write.version_mode = 'Follow Iteration'
    # write.compress_mode = 'DWAB'
    # write.frame_padding = 4
    # write.create_clip = False
    # write.shot_name = batch_name
    # write.source_timecode = current.clip.start_time
write_denoise.note = 'This Colour Mgmt node transforms AP1 (ACEScg) to Rec.709 in 32 bit'
write_denoise.note_collapsed = False

degrained_clip.name = 'Degrained_Clip'
degrained_clip.pos_x = color_mgnt_2.pos_x + 1000
degrained_clip.pos_y = color_mgnt_2.pos_y

pre_comp.name = 'Pre_Comp'
pre_comp.pos_x = write_denoise.pos_x + 1000
pre_comp.pos_y = write_denoise.pos_y

match_grain.name = 'Match_Noise'
match_grain.pos_x = write_denoise.pos_x + 1400
match_grain.pos_y = write_denoise.pos_y - 400

match_grain_compass.name = 'Match_Grain_Pipeline'
match_grain_compass.pos_x = denoise_compass.pos_x + 2000
match_grain_compass.pos_y = denoise_compass.pos_y
match_grain_compass.height = 800
match_grain_compass.width = 800

#Connect Nodes
# flame.batch.connect_nodes(current, "Default", plate, "Default")
flame.batch.connect_nodes(original_clip, "Default", color_mgnt_1, "Default")
flame.batch.connect_nodes(color_mgnt_1, "Default", ofx_1, "Default")
flame.batch.connect_nodes(ofx_1, "Default", color_mgnt_2, "Default")
flame.batch.connect_nodes(color_mgnt_2, "Default", write_denoise, "Default")
flame.batch.connect_nodes(pre_comp, "Default", match_grain, "Front")
flame.batch.connect_nodes(degrained_clip, "Default", match_grain, "Degrained Clip")
flame.batch.connect_nodes(original_clip, "Default", match_grain, "Original Clip")
