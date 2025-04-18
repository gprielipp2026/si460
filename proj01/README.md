# Minimum Specifications (Statement of Work)

1. A Single Player - This is the game character that the user will play, which must:
    a. Player must be a sprite which is normally in an animation loop
        `
        Player object has an animation loop that changes based on the keys pressed.
        `
    b. Sprites should face in the direction of movement
        `
        This is handled in the same way the animation loop gets updated.
        `
    c. Be movable in the x and y directions, z is optional, controlled by keyboard input 
       (use the arrow keys as well as any other keys you need for actions)
        `
        This is handled similarly to the animation loop update. The Player has flags to determine when positions should change that get updated during collide events and on draw/update.
        `
    d. Have the ability to "shoot" or "throw" something that can harm enemies.
        `
        A key will be able to be pressed that creates a new weapon (that is a Player without gravity or keyboard input) that moves in one direction until it hits something or goes off screen.
        `
    e. Must have the concept of HP (Health Points) so that a single hit to the player 
       doesnt cause insta-death
        `
        This is a field in the Player object.
        `
    f. Movement must be somewhat grounded in reality, (ex. jumps, running, walking, 
       flying, should all look like one would expect)
        `
        Fine tuning of the constants and when certain flags need to be applied is what is done.
        `

2. Enemies - These are the opposing players that the computer runs, which must:
    a. Enemy must be a sprite which is normally in an animation loop
        `
        An Enemy is just a Player with a different name and "AI" instead of keyboard input.
        `
    b. Sprites should face in the direction of movement
        `
        Handled in the Player code.
        `
    c. Be movable in the x and y directions, z is optional.
        `
        Enemy will walk forward unless it will fall or hit a wall, then it will turn around and proceed.
        `
    d. Have some ability to attack the Player
        `
        The Enemy will "attack" the Player by walking into them (collide).
        `
    e. Must have the concept of HP (Health Points) so that a single hit from the 
       player doesnt cause insta-death
        `
        Enemies will be terminated with 2 weapon collisions or 1 sword sweep attack.
        `
    f. Movement must be somewhat grounded in reality, (ex. jumps, running, walking, 
       flying, should all look like one would expect)
        `
        Movement is based on if it can walk forward or not, then turning around if it can't.
        `
    g. There must be some movement to the enemies
        `
        Movement is based on if it can walk forward or not, then turning around if it can't.
        `

3. Environment - The environment that the game takes place in must:
    a. Have some obstacles such as terrain that the Players and Enemies cant move through
        `
        This is handled in the Player object. It can be defined in the config file.        
        `
