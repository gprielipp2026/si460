# SI460 pyglet sprite loading library

# pyglet and system libraries
import pyglet, os

# Function to load all images from all subdirs in sprite directory
# Returns a dictionary of the form:
#    {'hero': {'Run':{'Left':  [...array of images facing left...],
#                     'Right': [...array of images facing right...]}}}
def loadAllImages(filepath="mylevel/sprites"):
    dirs = os.listdir(filepath)
    results = {}
    for d in dirs:
        results[d] = loadImages(filepath+'/'+d)
    return results

# Function to load all images within a subdirectory
# Returns a dictionary of the form:
#    {'Run':{'Left':  [...array of images facing left...],
#            'Right': [...array of images facing right...]}}
def loadImages(filepath="mylevel/sprites/hero"):
    files = os.listdir(filepath)
    files.sort()
    results = {}

    # Lets fix the numbering problem (1, 10, 2, 3, etc.)
    for f in files:
        if f.find('.png') != -1 and f.find('(') != -1:
            mode = f.split('(')[0].strip()
            seqnum = f.split(')')[0].split('(')[1].strip().zfill(2)
            if not mode in results:
                results[mode] = {'Right':{}, 'Left':{}}
            results[mode]['Right'][seqnum] = filepath+'/'+f
            results[mode]['Left'][seqnum] = filepath+'/'+f
        elif f.find('.png') != -1:
            mode = f.split('.png')[0].strip()
            seqnum = "00"
            if not mode in results:
                results[mode] = {'Right':{}, 'Left':{}}
            results[mode]['Right'][seqnum] = filepath+'/'+f
            results[mode]['Left'][seqnum] = filepath+'/'+f

    # Now lets start the process to load the actual images, now that
    # the order will be correct.
    for mode in results:
        right = []
        left = []
        for seqnum in sorted(results[mode]['Right'].items()):
            r = pyglet.resource.image(seqnum[1], flip_x=False)
            l = pyglet.resource.image(seqnum[1], flip_x=True)
            r.anchor_x = r.width / 2.0
            l.anchor_x = l.width / 2.0
            right.append(r)
            left.append(l)
        results[mode] = {'Right': right, 'Left': left}

    # return our results
    return results

# Build and return a configured sprite
def buildSprite(sprites={}, character="hero", mode="Run", facing="Right",
                animationSpeed=0.05, animationScale=0.15, animationLoop=True,
                animationX=400, animationY=300):

    # Grab the correct sequence of images
    playerSequence = sprites[character][mode][facing]

    # Build the pyglet animation sequence
    playerAnimation = pyglet.image.Animation.from_image_sequence(playerSequence,
                                                                 animationSpeed,
                                                                 animationLoop)
    # Create the sprite from the animation sequence
    playerSprite = pyglet.sprite.Sprite(playerAnimation,
                                        x=animationX,
                                        y=animationY)
    # Set the player's scale
    playerSprite.scale = animationScale

    return playerSprite

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    loadTest = loadImages()
    imagesTest = loadAllImages()
