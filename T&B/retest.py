import replicate
import os

string_dialogue = "You are a helpful programmer. You do not respond as 'User' or pretend to be 'User'. You only respond me in python code.I will give you a piece of python code to complete it. Please give me the complete code."
python_code="""
from ArmEnv_3D_ori import ArmEnv_3D

Arm=ArmEnv_3D([0, 5.5, 5.5, 8.5], True)
Arm.target=[0, 0, 19.5]

path=[]
#path.append(Arm.moveto(target_point, steps))
#complete code from here

for pa in path:
    for po in pa:
        Arm.forward_kinematics(po)
        Arm.updatePicture()
"""
string_dialogue2="please complete this python code by using moveto function, it can move the top of the robot arm to target point. for example: if i want to move the top of the arm to (5, 5, 5) in 25 steps, just use path.append(Arm.moveto([5, 5, 5], 25))"
pos_input="the ball is at(5, 5, 5), the the top of the tower is at(5, 5, 10)"
prompt_input="please modify the code to let robot arm grab the ball to the top of the tower."

os.environ["REPLICATE_API_TOKEN"] = "r8_HuU6MteQQJFci9bJtZzGBzhDut60vOO22Utb5"
output = replicate.run(
    "meta/llama-2-70b:a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00",
    input={"prompt": f"{string_dialogue}, origin python code:{python_code}, {string_dialogue2}, positions:{pos_input}, require:{prompt_input}, modified python code: ",
    "temperature":0.1, "top_p":0.9, "repetition_penalty":1})

# The meta/llama-2-70b model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
full=""
for item in output:
    # https://replicate.com/meta/llama-2-70b/versions/a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00/api#output-schema
    full+=item
print(full)