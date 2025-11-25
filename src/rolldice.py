import bpy
import random
import math

dice = bpy.data.objects["DICE"]  # change name

# pre-built rotations for faces
rotations = {
    1: (0, 0, 0),
    2: (math.radians(180), 0, 0),
    3: (0, math.radians(90), 0),
    4: (0, math.radians(-90), 0),
    5: (math.radians(90), 0, 0),
    6: (math.radians(-90), 0, 0)
}

result = random.randint(1, 6)
dice.rotation_euler = rotations[result]
print("RESULT:", result)
