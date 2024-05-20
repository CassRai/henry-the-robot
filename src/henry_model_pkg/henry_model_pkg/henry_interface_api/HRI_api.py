#HRI and OpenAI API client

#!/usr/bin/env python3

import threading

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import json
from openai import OpenAI
from openai import OpenAIError

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from ament_index_python.packages import get_package_share_directory

import os

class HRI:

    def __init__(self, node):

        self.client = OpenAI()
        self.node = node

        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.configure(bg="white")
        self.root.title("Little Henry")

        self.frame = tk.Frame(self.root, bg="#3366ff")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.label_1 = tk.Label(self.frame, text="What would you like 'Henry The Robot' to do?", font=('Arial', 20), bg="#3366ff")
        self.label_1.place(relx=0.5, rely=0.2, anchor="center")

        self.label_2 = tk.Label(self.frame, text="Please speak as naturally as possible!", font=('Arial', 12), bg="#3366ff")
        self.label_2.place(relx=0.5, rely=0.3, anchor="center")

        self.textbox = tk.Text(self.frame, height=3,font=('Arial', 12))
        self.textbox.place(relx=0.5, rely=0.6, anchor="center")
        self.textbox.config(width=60)

        self.perform_btn = tk.Button(self.frame, text="Perform Task",font=('Arial', 15), bg="yellow", command=self.send_input)
        self.perform_btn.place(relx=0.5, rely=0.8, anchor="center")


    def send_input(self):
        global user_prompt
        user_prompt = self.textbox.get(1.0,"end-1c")
        self.textbox.delete("1.0", "end") 
        #using a thread to allow api to handle input without having to close GUI.
        # target - when thread starts will call api_process_input function - allow api to process prompt.
        threading.Thread(target=self.api_process_input, args=(user_prompt,)).start()
        print(user_prompt)

    def api_process_input(self, user_input):
        #wrapping around  a try-except block to provide error checking for api issues
        try:
            #"role": "system" = context information, gives information to model about the role they are playing.
            #"role": "user" = the actual user who is sending a request to chatGPT
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                temperature=0.3,
                messages=[
        {"role": "system", "content": "You are an assistant designed to create JSON output from a user's command to a 4 wheeled mobile robot called Henry in a Gazebo simulation"},
        {"role": "system", "content": "The JSON output you produce needs to be contextualised to Robot Operating System 2(ROS2)'s and Ignition Gazebo's twist data type format  "},
        {"role": "system", "content": """
        
        Here are some examples of twist messages and what they will make Henry do -
            {
            moves forward 1m/s whilst gently turning left: {
                "linear": {
                "x": 1.0,
                "y": 0.0,
                "z": 0.0
                },
                "angular": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.05
                }
            },
            "moves backward 1m/s whilst sharply turning right ": {
                "linear": {
                "x": -1.0,
                "y": 0.0,
                "z": 0.0
                },
                "angular": {
                "x": 0.0,
                "y": 0.0,
                "z": -0.2
                }
            },
            "moves forward very fast": {
                "linear": {
                "x": 20.0,
                "y": 0.0,
                "z": 0.0
                },
                "angular": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
                }
            },
            "stops abruptly": {
                "linear": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
                },
                "angular": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
                }
            }
            }
        
        So learn from the above twist messages and use them to help guide you into generating twist messages based on what the user types.
        For example moving Henry backwards very fast is not there but you can learn how to do that based on the mappings I have outlined.
        Another example of this, is moving in a circle - Henry can drive in a circle although not stated there.

        Also use your understanding of physics to guide you.

        If the user input can be converted to a twist message stick to this format:
        "linear": {
                "x": 
                "y": 
                "z": 
            },
            angular": {
                "x": 
                "y": 
                "z": 
            }
            """},
        
        {"role": "system", "content": """If a user input cannot be converted to a twist message or it is not possible for Henry to do something:
                                        Then produce a JSON output such as:
                                                {
                                                "bad_prompt": true,
                                                "message": "Henry cannot do this"
                                                }  
                                        But you do not have to follow this exactly - you can use the context of the prompt and be specific to each prompt - why can't Henry do it?.                                                                         
        """},

        {"role": "system", "content": "If a user references the world think of the limitations and possibilties of a generic an empty Gazebo simulation world with only Henry inside it"},
        
        {"role": "user", "content": user_prompt}
        ]
            )
            assistant_response = response.choices[0].message.content
            reply = json.loads(assistant_response)

            if "bad_prompt" in reply:
                self.display_error(reply["message"])

            else:
                linear_x = reply.get('linear', {}).get('x', 0)
                angular_z = reply.get('angular', {}).get('z', 0)
                self.display_response(reply)
                self.node.send_vel(linear_x, angular_z)
        
        except OpenAIError as ai_error:
            ai_response_msg = ai_error.body["message"]
            self.display_api_error

    def display_response(self, message):
        print("Command processed:", message)

    def display_error(self,message):
        messagebox.showerror("Error", message)

    def display_api_error(self, message):
        self.root.after(0, lambda: messagebox.showerror("Error", message))

class PromptPublisher(Node):
    def __init__(self):
        #calling init of rclpy Node
        super().__init__('prompt_publisher')
        self.cmd_vel_pub_ = self.create_publisher(Twist, '/cmd_vel', 10) #10 = queue size
        self.get_logger().info('prompt publisher Node has been started')

    def send_vel(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.timer_ = self.create_timer(0.5, lambda: self.cmd_vel_pub_.publish(msg))
        self.get_logger().info('Prompt has been published')


def run_ros():
    rclpy.spin(node)

def main():
    rclpy.init()
    global node
    node = PromptPublisher()
    hri = HRI(node)
    ros_thread = threading.Thread(target=run_ros)
    ros_thread.start()
    hri.root.mainloop()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
    