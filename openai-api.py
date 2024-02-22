import json
from openai import OpenAI
from shared_data import queue

client = OpenAI()

#"role": "system" = context information, gives information to model about the role they are playing.
#"role": "user" = us, the acc user who is sending a request to chatGPT

try:
    with open("user_input.txt", "r") as file:
        user_prompt = file.read().strip()
except FileNotFoundError:
    user_prompt = ""

response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  response_format={ "type": "json_object" },
  temperature=0.3,
  messages=[
    {"role": "system", "content": "You are an assistant designed to create JSON output from a user's command to a 4 wheeled mobile robot called Henry he has a camera so he can see where he is going"},
    {"role": "system", "content": "The JSON output you produce needs to be contextualised to Robot Operating System commands"},
    {"role": "system", "content": """
     
     Here are all the JSON outputs you can produce for a response, stick exactly to: forward, backward, turn_left and  turn_right.
        {
        "forward": {
            "linear": {
            "x": 1.0,
            "y": 0.0,
            "z": 0.0
            },
            "angular": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
            }
        },
        "backward": {
            "linear": {
            "x": -1.0,
            "y": 0.0,
            "z": 0.0
            },
            "angular": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
            }
        },
        "turn_left": {
            "linear": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
            },
            "angular": {
            "x": 0.0,
            "y": 0.0,
            "z": 1.0
            }
        },
        "turn_right": {
            "linear": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
            },
            "angular": {
            "x": 0.0,
            "y": 0.0,
            "z": -1.0
            }
        },
        "stop": {
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
        """},
    
    {"role": "system", "content": """If a user input cannot be converted to a JSON formatted: forward, backward, turn_left and  turn_right command
                                     Then produce a JSON output such as:
                                            {
                                            "bad_prompt": true,
                                            "message": "Henry cannot do this"
                                            }  
                                    But you do not have to follow this exactly - you can use the context of the prompt and be specific to each prompt - why can't Henry do it?.                                                                         
     """},

    {"role": "system", "content": "If a user references the world think of the limitations and possibilties of a generic blank empty ROS-Gazebo simulation world"},
     
    {"role": "user", "content": user_prompt}
    ]
)
  


assisant_response = response.choices[0].message.content
reply = json.loads(assisant_response)
print("Output:", assisant_response.strip("\n").strip())