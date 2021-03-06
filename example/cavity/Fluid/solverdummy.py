from __future__ import division

import numpy as np
import precice

configuration_file_name = "../precice-config.xml"
participant_name = "Fluid_Solver"
mesh_name = "Fluid_Nodes"
write_data_name = 'Force'
read_data_name = 'DisplacementDelta'

num_vertices = 576  # Number of vertices

solver_process_index = 0
solver_process_size = 1

interface = precice.Interface(participant_name, configuration_file_name,
                              solver_process_index, solver_process_size)

mesh_id = interface.get_mesh_id(mesh_name)
dimensions = interface.get_dimensions()

vertices = np.zeros((num_vertices, dimensions))
read_data = np.zeros((num_vertices, dimensions))
write_data = np.zeros((num_vertices, dimensions))

for x in range(num_vertices):
    for y in range(0, dimensions):
        vertices[x, y] = x
        read_data[x, y] = x
        write_data[x, y] = x

vertex_ids = interface.set_mesh_vertices(mesh_id, vertices)
read_data_id = interface.get_data_id(read_data_name, mesh_id)
write_data_id = interface.get_data_id(write_data_name, mesh_id)

dt = interface.initialize()

while interface.is_coupling_ongoing():
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        print("DUMMY: Writing iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())

    if interface.is_read_data_available():
        read_data = interface.read_block_vector_data(read_data_id, vertex_ids)

    write_data = read_data + 1

    if interface.is_write_data_required(dt):
        interface.write_block_vector_data(
            write_data_id, vertex_ids, write_data)

    print("DUMMY: Advancing in time")
    dt = interface.advance(dt)

    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())

interface.finalize()
print("DUMMY: Closing python solver dummy...")
