from openai import OpenAI

class chatGPT:
    def __init__(self, idx):

        self.client = OpenAI(
            # This is the default and can be omitted
            api_key="",
        )

        if idx==0:
            pass
        elif idx==1:
            self.hader="""
The following functions are available:
arm.draw(from, to): Let the arm draw a straight line from from to to, such as draw([0.0, 0.0], [5.0, 5.0]). 
The upper limit is 5,
the lower limit is 0.
Please help me to control the robotic arm using the above functions.

Please help me use the above functions to control the robot arm, and do not output other text other than the above functions. (Use "," to separate each step)
"""
        elif idx==2:
            self.hader="""
The following functions are available:


aim(color): Let the robot aim at a block of a specific color. color option: red, blue.
grab: Make the robot arm grab the block and put it down.
reset: Return the robotic arm to its initial position (needs to be executed before each aiming).

Please help me use the above functions to control the robot arm, and do not output other text other than the above functions. (Use "," to separate each step)
"""
        elif idx==3:
            self.hader="""
The following functions are available:

aim(color): Let the robot aim at a block of a specific color.(Needs to be executed before grab) color option: red, blue.
grab(): Make the robot arm grab the block up.(Needs to be executed before load)
putdown(): Make the robot arm put the block down.
load(): Place the block on the car body.(Blocks will block the lens, so you need to keep the robotic arm clear of anything when looking forward.)
unload(): Remove the block from the car body, will block the lens.
lookForward(): Make the camera mounted on the robotic arm look forward. (Needs to be executed before driving the wheels)
reset(): Make the camera mounted on the robotic arm look downward. (Needs to be executed before aiming)

GoForward(): Drive the wheels forward, and stop when encountering a block.(Needs to be executed before skip)
Skip(): Drive the wheels to skip the block ahead. 

here is the sample commands to skip the green block and grab the red block and place it in front of the blue block.:
lookForward(), GoForward(), Skip(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), reset(), unload(), putdown() 

Please help me use the above functions to control the robot arm, and do not output other text other than the above functions. (Use "," to separate each step)
"""


    def ask(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": self.hader}, {"role": "user", "content": "Task: "+prompt}]
        )
        return response.choices[0].message.content.strip()

if __name__=="__main__":
    import time
    for i in range(10):
        chat_gpt=chatGPT(2)
        q1="Draw a star"
        q2="Please grab the red block and then grab the blue placing block."
        q3="There are three blocks in front of you. The colors are red, green, and blue in order. Please grab the red block and skip the green block and place it in front of the blue block."
        response=chat_gpt.ask(q2)
        print(response)
        time.sleep(1)

#Task 3
#gpt-4o
"reset,aim(red),grab,reset,aim(blue),grab"
"reset,aim(red),grab,reset,aim(blue),grab"
"reset,aim(red),grab,reset,aim(blue),grab"
"reset,aim(red),grab,reset,aim(blue),grab"
"reset, aim(red), grab, reset, aim(blue), grab"
"reset,aim(red),grab,reset,aim(blue),grab"
"reset,aim(red),grab,reset,aim(blue),grab"
"reset,aim(red),grab,reset,aim(blue),grab"
"reset,aim(red),grab,reset,aim(blue),grab"
"reset,aim(red),grab,reset,aim(blue),grab"

"9/10"

#gpt-3.5-turbo
"aim(red), grab, reset, aim(blue), grab"
"aim(red), grab, reset, aim(blue), grab"
"reset, aim(red), grab, reset, aim(blue), grab"
"X aim(red), grab, aim(blue), grab"
"aim(red), grab, reset, aim(blue), grab"
"aim(red), grab, reset, aim(blue), grab"
"aim(red), grab, reset, aim(blue), grab"
"aim(red), grab, reset, aim(blue), grab"
"X aim(red), grab, aim(blue), grab"
"aim(red), grab, reset, aim(blue), grab"

"7/10"

#Task 4
#gpt-4o
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), reset(), aim(red), grab(), lookForward(), GoForward(), Skip(), reset(), aim(blue), putdown()"
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), reset(), unload(), putdown()"

"7/10"

#gpt-3.5-turbo
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"lookForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), Skip(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), reset(), aim(red), grab(), load(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), reset(), aim(red), grab(), load(), GoForward(), Skip(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), Skip(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), Skip(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), reset(), aim(red), grab(), load(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), GoForward(), GoForward(), reset(), aim(red), grab(), load(), lookForward(), GoForward(), reset(), unload(), putdown()"
"X lookForward(), GoForward(), reset(), aim(red), grab(), load(), GoForward(), reset(), Skip(), GoForward(), reset(), unload(), putdown()"

"2/10"