from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():

    # Set the path for the URDF file
    pkg_path = get_package_share_directory('henry_model_pkg')
    xacro_file_path = os.path.join(pkg_path, 'urdf', 'henry1.5.xacro')
    robot_description_raw = xacro.process_file(xacro_file_path).toxml()

    urdf_file_path = os.path.join(pkg_path, 'urdf', 'henry1.5.urdf')
    with open(urdf_file_path, 'w') as urdf_file:
        urdf_file.write(robot_description_raw)


    node_ignition_gazebo = ExecuteProcess(
        cmd=[
            'ign', 'gazebo', '-r', 'empty.sdf'
        ],
        output='screen'
    )

    # Node to spawn Henry into Gazebo
    node_spawn_henry = Node(
        package='ros_gz_sim',       
        executable='create',
        arguments=['-file', urdf_file_path, '-name', 'Henry-1.5', '-z', '1'],
        output='screen'
    )

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
                     'use_sim_time': True}]
    )

    # ] = bridge from ROS2 to Ignition Gazebo
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'
        ],
        parameters=[{
            'qos_overrides./cmd_vel.subscriber.reliability': 'reliable'
        }],
        output='screen'
)


    
    # Assemble everything into a launch description
    ld = LaunchDescription([
        node_ignition_gazebo,
        node_spawn_henry,
        node_robot_state_publisher,
        bridge
    ])

    return ld
