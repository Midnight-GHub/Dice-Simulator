# rolldice_playback.py
import bpy
import mathutils
import random
import time
import sys

DICE_NAME = "DICE"

# Parameters
PLAY_SECONDS = 4.0         # how long to allow the roll (max)
POLL_INTERVAL = 0.05       # seconds between checks
SETTLE_THRESHOLD = 0.08    # linear velocity magnitude considered "settled"
MAX_WAIT = 8.0             # hard timeout in seconds

# get dice
dice = bpy.data.objects.get(DICE_NAME)
if dice is None:
    print("RESULT: -1", flush=True)
    sys.stdout.flush()
    raise SystemExit

scene = bpy.context.scene

# ensure rigidbody active
if dice.rigid_body is None:
    bpy.context.view_layer.objects.active = dice
    bpy.ops.rigidbody.object_add()

dice.rigid_body.type = 'ACTIVE'
# ensure physics enabled
dice.rigid_body.kinematic = False

# reset frame and place dice above plane
scene.frame_set(1)
dice.location = (0.0, 0.0, 2.0)
dice.rotation_euler = (
    random.uniform(0, 6.283185307179586),
    random.uniform(0, 6.283185307179586),
    random.uniform(0, 6.283185307179586),
)

# apply randomized velocities (impulse-like)
import math
lin = mathutils.Vector((
    random.uniform(-3.5, 3.5),
    random.uniform(-3.5, 3.5),
    random.uniform(10.0, 16.0)
))
ang = mathutils.Vector((
    random.uniform(-12.0, 12.0),
    random.uniform(-12.0, 12.0),
    random.uniform(-12.0, 12.0)
))
try:
    dice.rigid_body.linear_velocity = lin
    dice.rigid_body.angular_velocity = ang
except Exception:
    # if direct assignments unavailable, you can set via object properties as fallback
    pass

bpy.context.view_layer.update()

# Start viewport playback (so the physics runs in viewport)
if not bpy.context.screen.is_animation_playing:
    bpy.ops.screen.animation_play()

start_time = time.time()
settled = False

# Poll until the dice slow down (settle) or timeout
while True:
    # let Blender run for a short interval
    time.sleep(POLL_INTERVAL)

    # update depsgraph so physics values are up-to-date
    bpy.context.view_layer.update()

    # read linear velocity
    vel = 0.0
    try:
        vel = dice.rigid_body.linear_velocity.length
    except Exception:
        # fallback: compute small approximated speed (rare)
        vel = 0.0

    # If below threshold for a little while, consider settled
    if vel < SETTLE_THRESHOLD:
        # give a short grace to ensure it's really stable
        time.sleep(0.25)
        bpy.context.view_layer.update()
        try:
            if dice.rigid_body.linear_velocity.length < SETTLE_THRESHOLD:
                settled = True
                break
        except Exception:
            settled = True
            break

    # timeout guard
    if time.time() - start_time > MAX_WAIT:
        break

# Stop playback (leave Blender usable)
if bpy.context.screen.is_animation_playing:
    bpy.ops.screen.animation_play()

# Compute top face by checking local normals in world space
up = mathutils.Vector((0, 0, 1))

# Adjust normals depending on your dice orientation.
# These are typical axes; if your dice has an offset/rotation, you may need to change these.
normals = {
    1: mathutils.Vector((0, 0, 1)),
    2: mathutils.Vector((0, 0, -1)),
    3: mathutils.Vector((0, 1, 0)),
    4: mathutils.Vector((0, -1, 0)),
    5: mathutils.Vector((1, 0, 0)),
    6: mathutils.Vector((-1, 0, 0)),
}

mat = dice.matrix_world.to_3x3()
best_face = None
best_dot = -9.0
for f, n in normals.items():
    world_n = mat @ n
    dot = world_n.dot(up)
    if dot > best_dot:
        best_dot = dot
        best_face = f

print(f"RESULT: {best_face}", flush=True)
sys.stdout.flush()

# OPTIONAL: leave Blender open for teacher to inspect
# time.sleep(5)   # if you want a pause
# DO NOT call bpy.ops.wm.quit_blender() if you want Blender to stay open.
