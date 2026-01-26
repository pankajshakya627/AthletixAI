"""
Exercise Details Library - Contains detailed instructions for common exercises.

Used by program_builder.py to populate description, steps, and breathing_guide fields.
"""

# Exercise details lookup - maps exercise names to their detailed instructions
EXERCISE_DETAILS = {
    # =========================================================================
    # WARMUP EXERCISES
    # =========================================================================
    "arm circles": {
        "description": "A dynamic warmup exercise that loosens the shoulder joints and increases blood flow to the upper body.",
        "steps": [
            "Stand with feet shoulder-width apart, arms extended straight out to the sides at shoulder height",
            "Make small circular motions with your arms, gradually increasing the size of the circles",
            "After 15 seconds, reverse the direction of the circles",
            "Keep your core engaged and maintain good posture throughout"
        ],
        "breathing_guide": "Breathe naturally and steadily throughout the movement"
    },
    "leg swings": {
        "description": "A dynamic stretch that opens up the hips and prepares the legs for lower body exercises.",
        "steps": [
            "Stand next to a wall or support, holding it for balance with one hand",
            "Keep your standing leg slightly bent and core engaged",
            "Swing the outside leg forward and backward in a controlled motion",
            "Gradually increase the range of motion as your muscles warm up",
            "Switch sides and repeat"
        ],
        "breathing_guide": "Exhale as the leg swings forward, inhale as it swings back"
    },
    "cat-cow stretch": {
        "description": "A gentle spinal mobility exercise that warms up the back and improves flexibility.",
        "steps": [
            "Start on all fours with hands under shoulders and knees under hips",
            "Cow: Inhale, drop your belly, lift your chest and tailbone, look slightly upward",
            "Cat: Exhale, round your spine toward ceiling, tuck chin to chest, draw navel in",
            "Flow smoothly between positions, moving with your breath"
        ],
        "breathing_guide": "Inhale during cow position (back arched), exhale during cat position (back rounded)"
    },
    "shoulder rolls": {
        "description": "A simple warmup to release tension in the shoulders and upper back.",
        "steps": [
            "Stand or sit with arms relaxed at your sides",
            "Lift shoulders up toward your ears",
            "Roll them back and down in a circular motion",
            "Complete all reps in one direction, then reverse"
        ],
        "breathing_guide": "Inhale as shoulders rise, exhale as they roll back and down"
    },
    "hip circles": {
        "description": "A mobility exercise that loosens the hip joints and improves range of motion.",
        "steps": [
            "Stand with feet hip-width apart, hands on hips for balance",
            "Make large circular motions with your hips, as if hula hooping",
            "Keep your upper body relatively stable",
            "Complete all reps in one direction, then reverse"
        ],
        "breathing_guide": "Breathe naturally and steadily throughout the movement"
    },
    "inchworm": {
        "description": "A full-body warmup that stretches the hamstrings and activates the core and shoulders.",
        "steps": [
            "Stand with feet hip-width apart, bend at the waist and place hands on floor",
            "Walk your hands forward until you're in a high plank position",
            "Hold briefly, then walk your feet toward your hands with small steps",
            "Stand up and repeat"
        ],
        "breathing_guide": "Exhale as you walk hands out, inhale as you walk feet in"
    },
    "band pull-apart": {
        "description": "A rotator cuff and rear delt warmup that prepares the shoulders for pressing movements.",
        "steps": [
            "Hold a resistance band with both hands, arms extended in front at shoulder height",
            "Keep arms straight and pull the band apart by squeezing shoulder blades together",
            "Bring the band to your chest, pause briefly",
            "Slowly return to starting position with control"
        ],
        "breathing_guide": "Exhale as you pull the band apart, inhale as you return"
    },
    "push-up to downward dog": {
        "description": "A dynamic flow that warms up the chest, shoulders, and hamstrings.",
        "steps": [
            "Start in a high plank position with hands shoulder-width apart",
            "Perform one push-up by lowering chest to the floor and pressing back up",
            "Push hips up and back into downward dog position, heels pressing toward floor",
            "Hold briefly, then flow back into plank and repeat"
        ],
        "breathing_guide": "Inhale in plank, exhale down in push-up, inhale up, exhale into downward dog"
    },
    "dead hang": {
        "description": "A passive stretch that decompresses the spine and stretches the lats and shoulders.",
        "steps": [
            "Grab a pull-up bar with an overhand grip, hands shoulder-width apart",
            "Let your body hang with arms fully extended",
            "Relax your shoulders and let them stretch naturally",
            "Keep your core slightly engaged to prevent excessive swinging"
        ],
        "breathing_guide": "Breathe deeply and slowly, relaxing more with each exhale"
    },
    
    # =========================================================================
    # COMPOUND MOVEMENTS
    # =========================================================================
    "squat": {
        "description": "The king of lower body exercises, targeting quads, glutes, and hamstrings while building overall leg strength and power.",
        "steps": [
            "Stand with feet shoulder-width apart, toes pointed slightly outward (15-30 degrees)",
            "Brace your core, take a deep breath, and begin by pushing hips back and bending knees",
            "Descend until thighs are at least parallel to the ground, keeping chest up and back neutral",
            "Drive through your heels to return to standing, squeezing glutes at the top",
            "Keep knees tracking over toes throughout the movement"
        ],
        "breathing_guide": "Take a deep breath and brace at the top, hold during descent, exhale powerfully as you stand"
    },
    "bodyweight squat": {
        "description": "A fundamental movement pattern that builds leg strength and reinforces proper squat mechanics.",
        "steps": [
            "Stand with feet shoulder-width apart, arms extended in front for balance",
            "Push hips back and bend knees to lower your body",
            "Descend until thighs are parallel to the ground or as low as comfortable",
            "Keep chest up, core braced, and weight in your heels",
            "Drive through heels to return to standing"
        ],
        "breathing_guide": "Inhale as you lower down, exhale as you push back up"
    },
    "goblet squat": {
        "description": "A beginner-friendly weighted squat variation that teaches proper form while building leg strength.",
        "steps": [
            "Hold a dumbbell or kettlebell at chest height with both hands, elbows pointing down",
            "Stand with feet slightly wider than shoulder-width, toes pointed slightly out",
            "Push hips back and squat down, keeping the weight close to your chest",
            "Descend until thighs are at least parallel, using your elbows to push knees out",
            "Drive through heels to stand, squeezing glutes at the top"
        ],
        "breathing_guide": "Inhale as you squat down, exhale as you drive up"
    },
    "bench press": {
        "description": "The primary chest builder that also develops the front deltoids and triceps.",
        "steps": [
            "Lie on bench with eyes under the bar, feet flat on floor, back slightly arched",
            "Grip the bar slightly wider than shoulder-width, unrack and position over mid-chest",
            "Lower the bar to your mid-chest with control, tucking elbows at about 45 degrees",
            "Touch your chest lightly, then press the bar up and slightly back",
            "Lock out at the top with the bar over your shoulders"
        ],
        "breathing_guide": "Inhale as you lower the bar to your chest, exhale as you press up"
    },
    "deadlift": {
        "description": "The ultimate full-body strength builder, primarily targeting the posterior chain including glutes, hamstrings, and back.",
        "steps": [
            "Stand with feet hip-width apart, bar over mid-foot, shins nearly touching the bar",
            "Hinge at hips to grip bar just outside knees with either double overhand or mixed grip",
            "Drop hips, lift chest, create tension by pulling slack out of the bar",
            "Drive through the floor, keeping the bar close to your body as you stand",
            "Lock out at the top by squeezing glutes, then reverse the movement to lower"
        ],
        "breathing_guide": "Take a deep breath and brace before the lift, exhale at lockout or on the way down"
    },
    "overhead press": {
        "description": "A fundamental pressing movement that builds shoulder strength and stability.",
        "steps": [
            "Stand with feet shoulder-width apart, bar resting on front shoulders",
            "Grip bar slightly wider than shoulders, squeeze glutes and brace core",
            "Press the bar straight up, moving your head back slightly as the bar passes",
            "Lock out with the bar directly over your head and shoulders",
            "Lower with control back to the starting position"
        ],
        "breathing_guide": "Inhale at the bottom, brace, then exhale as you press the bar overhead"
    },
    "barbell row": {
        "description": "A compound back exercise that builds thickness in the lats, rhomboids, and rear delts.",
        "steps": [
            "Stand with feet hip-width apart, holding the bar with overhand grip",
            "Hinge at hips until torso is roughly 45 degrees, letting bar hang at arm's length",
            "Pull the bar to your lower chest/upper abdomen, driving elbows back",
            "Squeeze shoulder blades together at the top, pause briefly",
            "Lower with control and repeat"
        ],
        "breathing_guide": "Exhale as you row the bar up, inhale as you lower it"
    },
    "pull-up": {
        "description": "The ultimate bodyweight back exercise that builds lat width and overall upper body pulling strength.",
        "steps": [
            "Hang from a bar with hands slightly wider than shoulder-width, palms facing away",
            "Engage your lats by depressing your shoulders (pulling them down and back)",
            "Pull yourself up by driving elbows down toward your hips",
            "Continue until chin clears the bar, pause briefly at the top",
            "Lower with control until arms are fully extended"
        ],
        "breathing_guide": "Exhale as you pull up, inhale as you lower"
    },
    "chin-up": {
        "description": "A pulling exercise that emphasizes the biceps while still heavily targeting the lats.",
        "steps": [
            "Hang from a bar with hands shoulder-width apart, palms facing toward you",
            "Engage your back by pulling shoulders down and back",
            "Pull yourself up by driving elbows down and back",
            "Continue until chin clears the bar, squeezing biceps at the top",
            "Lower with control until arms are fully extended"
        ],
        "breathing_guide": "Exhale as you pull up, inhale as you lower"
    },
    
    # =========================================================================
    # PUSH EXERCISES
    # =========================================================================
    "push-up": {
        "description": "A classic bodyweight exercise that builds chest, shoulder, and tricep strength.",
        "steps": [
            "Start in a high plank with hands slightly wider than shoulders, body in a straight line",
            "Lower your body by bending elbows, keeping them at about 45 degrees from your body",
            "Descend until chest nearly touches the floor",
            "Push through your palms to return to starting position",
            "Keep core tight and hips level throughout"
        ],
        "breathing_guide": "Inhale as you lower, exhale as you push up"
    },
    "incline dumbbell press": {
        "description": "An upper chest-focused pressing movement that builds the clavicular head of the pectorals.",
        "steps": [
            "Set bench to 30-45 degree incline, sit with dumbbells on thighs",
            "Lie back and press dumbbells to arm's length, palms facing forward",
            "Lower dumbbells to the sides of your upper chest with control",
            "Press back up, bringing dumbbells together at the top without clanking",
            "Squeeze chest at the top, then repeat"
        ],
        "breathing_guide": "Inhale as you lower the dumbbells, exhale as you press up"
    },
    "dumbbell shoulder press": {
        "description": "A shoulder-building exercise that allows for natural arm path and improved muscle activation.",
        "steps": [
            "Sit or stand with dumbbells at shoulder height, palms facing forward",
            "Press dumbbells overhead, bringing them together at the top",
            "Lower with control back to shoulder height",
            "Keep core engaged and avoid arching your lower back excessively"
        ],
        "breathing_guide": "Exhale as you press up, inhale as you lower"
    },
    "dumbbell lateral raise": {
        "description": "An isolation exercise that targets the lateral (side) head of the deltoids for wider shoulders.",
        "steps": [
            "Stand with feet hip-width apart, dumbbells at your sides, slight bend in elbows",
            "Raise arms out to the sides until they're parallel to the floor",
            "Lead with your elbows and keep them slightly bent throughout",
            "Lower with control, don't just drop the weights",
            "Avoid using momentum or swinging"
        ],
        "breathing_guide": "Exhale as you raise the weights, inhale as you lower"
    },
    "dumbbell flyes": {
        "description": "A chest isolation exercise that emphasizes the stretch and contraction of the pectoral muscles.",
        "steps": [
            "Lie on a flat bench with dumbbells pressed up, palms facing each other",
            "With a slight bend in elbows, lower dumbbells out to the sides in an arc",
            "Lower until you feel a stretch in your chest, keeping elbows slightly bent",
            "Squeeze chest to bring dumbbells back up in the same arc motion",
            "Avoid going too deep if you have shoulder issues"
        ],
        "breathing_guide": "Inhale as you lower the weights, exhale as you bring them together"
    },
    "cable crossover": {
        "description": "A cable chest exercise that provides constant tension throughout the range of motion.",
        "steps": [
            "Set pulleys to high position, grab handles and step forward into a split stance",
            "Start with arms out to sides, slight bend in elbows",
            "Bring hands together in front of your body in a hugging motion",
            "Squeeze chest at the bottom, pause briefly",
            "Return to starting position with control"
        ],
        "breathing_guide": "Exhale as you bring hands together, inhale as you open up"
    },
    "tricep pushdown": {
        "description": "An isolation exercise that targets all three heads of the triceps using a cable machine.",
        "steps": [
            "Stand facing a cable machine with a straight or V-bar attachment at chest height",
            "Grip the bar, tuck elbows at your sides, and keep them stationary",
            "Push the bar down by extending your elbows until arms are straight",
            "Squeeze triceps at the bottom, pause briefly",
            "Return with control, stopping when forearms are parallel to the floor"
        ],
        "breathing_guide": "Exhale as you push down, inhale as you return"
    },
    "overhead tricep extension": {
        "description": "A tricep exercise that emphasizes the long head of the triceps.",
        "steps": [
            "Hold a dumbbell with both hands overhead, arms fully extended",
            "Keep upper arms close to your head and stationary",
            "Lower the weight behind your head by bending at the elbows",
            "Lower until you feel a stretch in the triceps",
            "Extend arms back to starting position, squeezing triceps at the top"
        ],
        "breathing_guide": "Inhale as you lower the weight, exhale as you extend"
    },
    "diamond push-up": {
        "description": "A push-up variation that heavily emphasizes the triceps and inner chest.",
        "steps": [
            "Start in a push-up position with hands close together forming a diamond shape",
            "Keep elbows close to your body as you lower your chest toward your hands",
            "Lower until chest nearly touches your hands",
            "Push back up to starting position, squeezing triceps at the top",
            "Keep core engaged and body in a straight line throughout"
        ],
        "breathing_guide": "Inhale as you lower, exhale as you push up"
    },
    "tricep dip": {
        "description": "A compound exercise that builds tricep and lower chest strength using bodyweight.",
        "steps": [
            "Grip parallel bars and lift yourself to arm's length, arms locked",
            "Keep elbows close to body and lean slightly forward",
            "Lower your body by bending elbows until upper arms are parallel to floor",
            "Press back up to starting position, locking out at the top",
            "Avoid going too deep if you have shoulder issues"
        ],
        "breathing_guide": "Inhale as you lower, exhale as you push up"
    },
    
    # =========================================================================
    # PULL EXERCISES
    # =========================================================================
    "dumbbell row": {
        "description": "A unilateral back exercise that builds lat and rhomboid strength while allowing for a full range of motion.",
        "steps": [
            "Place one knee and hand on a bench, other foot on the floor for support",
            "Hold a dumbbell in the free hand, arm hanging straight down",
            "Pull the dumbbell to your hip, driving elbow up and back",
            "Squeeze your shoulder blade at the top, pause briefly",
            "Lower with control and repeat all reps before switching sides"
        ],
        "breathing_guide": "Exhale as you row up, inhale as you lower"
    },
    "seated cable row": {
        "description": "A seated pulling exercise that builds middle back thickness with constant cable tension.",
        "steps": [
            "Sit at a cable row station with feet on footrests, knees slightly bent",
            "Grip the handle with arms extended, chest up and back straight",
            "Pull the handle to your abdomen, driving elbows straight back",
            "Squeeze shoulder blades together at the end of the movement",
            "Extend arms with control, allowing a slight stretch in the lats"
        ],
        "breathing_guide": "Exhale as you pull, inhale as you extend"
    },
    "lat pulldown": {
        "description": "A machine-based vertical pulling exercise that develops lat width and upper back strength.",
        "steps": [
            "Sit at a lat pulldown machine, thighs secured under the pad",
            "Grip the bar wider than shoulder-width, arms fully extended",
            "Pull the bar down to your upper chest, driving elbows down and back",
            "Squeeze lats at the bottom, keeping torso relatively upright",
            "Control the bar back up until arms are fully extended"
        ],
        "breathing_guide": "Exhale as you pull down, inhale as you release"
    },
    "face pull": {
        "description": "An essential rear delt and rotator cuff exercise for shoulder health and posture.",
        "steps": [
            "Set a cable to face height with a rope attachment",
            "Grip the rope with palms facing inward, step back to create tension",
            "Pull the rope toward your face, separating your hands as you pull",
            "Finish with hands beside your ears, elbows high and back",
            "Squeeze rear delts and external rotators, then return with control"
        ],
        "breathing_guide": "Exhale as you pull toward your face, inhale as you extend"
    },
    "barbell curl": {
        "description": "The classic bicep builder that allows for heavy loading and progressive overload.",
        "steps": [
            "Stand with feet shoulder-width apart, grip bar with underhand grip at shoulder width",
            "Keep elbows pinned at your sides and upper arms stationary",
            "Curl the bar up by contracting biceps, moving only at the elbow",
            "Squeeze biceps at the top, pause briefly",
            "Lower with control, fully extending arms at the bottom"
        ],
        "breathing_guide": "Exhale as you curl up, inhale as you lower"
    },
    "hammer curl": {
        "description": "A bicep curl variation that emphasizes the brachialis and brachioradialis for fuller arm development.",
        "steps": [
            "Stand with dumbbells at your sides, palms facing your thighs (neutral grip)",
            "Keep elbows pinned at your sides throughout the movement",
            "Curl the dumbbells up while maintaining the neutral grip",
            "Squeeze at the top, then lower with control",
            "Avoid swinging or using momentum"
        ],
        "breathing_guide": "Exhale as you curl up, inhale as you lower"
    },
    "concentration curl": {
        "description": "An isolation exercise that provides peak contraction and maximum bicep squeeze.",
        "steps": [
            "Sit on a bench, spread legs, and brace back of upper arm against inner thigh",
            "Hold a dumbbell with arm fully extended toward the floor",
            "Curl the weight up, focusing on squeezing the bicep",
            "Hold the contraction at the top briefly",
            "Lower with control while maintaining contact with thigh"
        ],
        "breathing_guide": "Exhale as you curl up, inhale as you lower"
    },
    "reverse fly": {
        "description": "An isolation exercise for the rear deltoids and upper back muscles.",
        "steps": [
            "Hold dumbbells and bend forward at hips until torso is nearly parallel to floor",
            "Let arms hang straight down, palms facing each other",
            "Raise arms out to the sides until parallel to floor, leading with elbows",
            "Squeeze shoulder blades together at the top",
            "Lower with control to starting position"
        ],
        "breathing_guide": "Exhale as you raise the weights, inhale as you lower"
    },
    
    # =========================================================================
    # LEG EXERCISES
    # =========================================================================
    "romanian deadlift": {
        "description": "A hip-hinge exercise that primarily targets the hamstrings and glutes with a deep stretch.",
        "steps": [
            "Stand with feet hip-width apart, hold barbell or dumbbells in front of thighs",
            "Keep a slight bend in knees and maintain a flat back throughout",
            "Push hips back and lower the weight along your legs, feeling a stretch in hamstrings",
            "Lower until you feel a strong stretch or torso is nearly parallel to floor",
            "Drive hips forward to return to standing, squeezing glutes at top"
        ],
        "breathing_guide": "Inhale as you hinge down, exhale as you drive hips forward to stand"
    },
    "leg press": {
        "description": "A machine-based compound exercise that allows heavy loading of the quads, glutes, and hamstrings.",
        "steps": [
            "Sit in the leg press machine, place feet shoulder-width apart on the platform",
            "Release the safety handles and lower the platform toward your chest",
            "Lower until knees are at about 90 degrees without letting your lower back round",
            "Press through your heels and midfoot to push the platform away",
            "Stop just short of locking out your knees at the top"
        ],
        "breathing_guide": "Inhale as you lower the platform, exhale as you press up"
    },
    "leg curl": {
        "description": "An isolation exercise that targets the hamstrings through knee flexion.",
        "steps": [
            "Lie face down on a leg curl machine with pad just above your ankles",
            "Grip the handles for stability, keep hips pressed into the pad",
            "Curl your heels toward your glutes by bending at the knees",
            "Squeeze hamstrings at the top of the movement",
            "Lower with control to starting position"
        ],
        "breathing_guide": "Exhale as you curl up, inhale as you lower"
    },
    "leg extension": {
        "description": "An isolation exercise that targets the quadriceps muscles of the front thigh.",
        "steps": [
            "Sit in a leg extension machine with back against the pad",
            "Position the ankle pad just above your feet, grip the handles",
            "Extend your legs until they are straight, squeezing quads at the top",
            "Avoid locking the knees aggressively at the top",
            "Lower with control to starting position"
        ],
        "breathing_guide": "Exhale as you extend, inhale as you lower"
    },
    "bulgarian split squat": {
        "description": "A single-leg exercise that builds quad and glute strength while improving balance.",
        "steps": [
            "Stand about 2 feet in front of a bench, place top of rear foot on the bench",
            "Keep torso upright and core engaged",
            "Lower your body by bending the front knee until thigh is parallel to floor",
            "Keep front knee tracking over toes, not caving inward",
            "Drive through front heel to return to starting position"
        ],
        "breathing_guide": "Inhale as you lower, exhale as you push up"
    },
    "hip thrust": {
        "description": "The premier glute-building exercise that provides maximum glute activation.",
        "steps": [
            "Sit on the ground with upper back against a bench, feet flat on floor",
            "Place a barbell or dumbbell across your hips",
            "Drive through heels and thrust hips up until body forms a straight line from shoulders to knees",
            "Squeeze glutes hard at the top, pause briefly",
            "Lower hips back down with control"
        ],
        "breathing_guide": "Exhale as you thrust up, inhale as you lower"
    },
    "walking lunge": {
        "description": "A dynamic lower body exercise that builds legs while improving balance and coordination.",
        "steps": [
            "Stand tall with feet together, hands on hips or holding dumbbells at sides",
            "Take a large step forward with one leg",
            "Lower your body until both knees are bent at about 90 degrees",
            "Push through the front heel and bring the back leg forward into the next lunge",
            "Keep torso upright and core engaged throughout"
        ],
        "breathing_guide": "Inhale as you step and lower, exhale as you push off to the next step"
    },
    "calf raise": {
        "description": "An isolation exercise that targets the gastrocnemius and soleus muscles of the calves.",
        "steps": [
            "Stand on the edge of a platform with heels hanging off, toes on the platform",
            "Hold a wall or rail for balance, or hold dumbbells for resistance",
            "Lower heels below the platform to feel a stretch in the calves",
            "Push through the balls of your feet to rise up as high as possible",
            "Squeeze calves at the top, then lower with control"
        ],
        "breathing_guide": "Exhale as you rise up, inhale as you lower"
    },
    "glute bridge": {
        "description": "A beginner-friendly glute activation exercise that also targets hamstrings and core.",
        "steps": [
            "Lie on your back with knees bent, feet flat on floor hip-width apart",
            "Arms at sides with palms down for stability",
            "Push through heels to lift hips toward ceiling",
            "Squeeze glutes at the top, creating a straight line from shoulders to knees",
            "Lower with control and repeat"
        ],
        "breathing_guide": "Exhale as you lift hips, inhale as you lower"
    },
    
    # =========================================================================
    # CORE EXERCISES
    # =========================================================================
    "plank": {
        "description": "The foundational core exercise that builds isometric strength in the entire core and stabilizer muscles.",
        "steps": [
            "Start in a forearm plank position, elbows directly under shoulders",
            "Keep body in a straight line from head to heels",
            "Engage core by drawing navel toward spine and squeezing glutes",
            "Keep neck neutral, looking at the floor just ahead of your hands",
            "Hold the position without letting hips sag or pike up"
        ],
        "breathing_guide": "Breathe steadily and naturally throughout the hold - do not hold your breath"
    },
    "dead bug": {
        "description": "An anti-extension core exercise that teaches proper bracing while moving the limbs.",
        "steps": [
            "Lie on your back with arms extended toward ceiling and hips/knees at 90 degrees",
            "Press lower back firmly into the floor - maintain this contact throughout",
            "Slowly extend one arm overhead and the opposite leg out straight",
            "Return to starting position and repeat with the other arm and leg",
            "Move slowly and with control, keeping lower back pressed down"
        ],
        "breathing_guide": "Exhale as you extend the arm and leg, inhale as you return"
    },
    "world's greatest stretch": {
        "description": "A dynamic stretch that opens up the hips, thoracic spine, and hamstrings simultaneously.",
        "steps": [
            "Start in a push-up position, step right foot outside right hand",
            "Lower left forearm to the ground for a hip stretch",
            "Rotate torso and reach right arm toward the ceiling, opening up chest",
            "Return hand to floor and straighten front leg for a hamstring stretch",
            "Return to start and repeat on the other side"
        ],
        "breathing_guide": "Exhale as you rotate and open up, inhale to return"
    },
}


def get_exercise_details(exercise_name: str) -> dict:
    """
    Get detailed instructions for an exercise by name.
    
    Args:
        exercise_name: Name of the exercise (case-insensitive)
    
    Returns:
        Dictionary with description, steps, and breathing_guide, or empty dict if not found
    """
    # Try exact match first
    normalized_name = exercise_name.lower().strip()
    if normalized_name in EXERCISE_DETAILS:
        return EXERCISE_DETAILS[normalized_name]
    
    # Try partial match
    for key in EXERCISE_DETAILS:
        if key in normalized_name or normalized_name in key:
            return EXERCISE_DETAILS[key]
    
    return {}
