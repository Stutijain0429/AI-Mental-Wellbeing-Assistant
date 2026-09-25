import random


EMOTION_RESPONSES = {
    "joy": [
        {
            "message": "It's nice to hear that you're feeling positive.",
            "suggestion": "Take a moment to enjoy what's making you happy today."
        },
        {
            "message": "You seem to be having a good moment.",
            "suggestion": "You could write down what made today feel special."
        },
        {
            "message": "It sounds like something brought you some happiness.",
            "suggestion": "Try sharing that positive moment with someone you care about."
        },
        {
            "message": "I'm glad you're experiencing a positive feeling.",
            "suggestion": "Pause for a moment and appreciate how you're feeling right now."
        }
    ],

    "love": [
        {
            "message": "It sounds like you feel deeply connected to someone.",
            "suggestion": "Spend some meaningful time with the people you care about."
        },
        {
            "message": "There's a strong sense of affection in what you shared.",
            "suggestion": "Let someone you care about know that they matter to you."
        },
        {
            "message": "It sounds like you're feeling warmth and connection.",
            "suggestion": "Enjoy the little moments you share with people who are important to you."
        }
    ],

    "sadness": [
        {
            "message": "I'm sorry you're feeling low right now.",
            "suggestion": "Take things slowly and give yourself some space to breathe."
        },
        {
            "message": "It sounds like you're going through a difficult moment.",
            "suggestion": "You don't have to solve everything at once. Focus on one small thing you can do right now."
        },
        {
            "message": "It seems like things are feeling a little heavy today.",
            "suggestion": "Try taking a short break, getting some fresh air, or talking to someone you trust."
        },
        {
            "message": "Some days can feel harder than others, and that's okay.",
            "suggestion": "Be gentle with yourself and focus on getting through the next small step."
        },
        {
            "message": "It sounds like you could use a little emotional space.",
            "suggestion": "Take a few slow breaths and do something small that usually helps you feel comfortable."
        }
    ],

    "anger": [
        {
            "message": "It sounds like something has really frustrated you.",
            "suggestion": "Give yourself some space before reacting. A short walk or a few slow breaths may help."
        },
        {
            "message": "You seem to be dealing with a lot of frustration right now.",
            "suggestion": "Try stepping away from the situation for a few minutes before deciding what to do next."
        },
        {
            "message": "It sounds like something has upset you deeply.",
            "suggestion": "Take a moment to identify what specifically triggered the feeling."
        },
        {
            "message": "Strong emotions can make situations feel even more intense.",
            "suggestion": "Pause, breathe slowly, and give yourself time before responding."
        }
    ],

    "fear": [
        {
            "message": "It sounds like you're feeling worried or afraid.",
            "suggestion": "Focus on what you can control right now and take things one step at a time."
        },
        {
            "message": "Something seems to be making you feel uncertain.",
            "suggestion": "Try separating what you know from what you're worried might happen."
        },
        {
            "message": "It sounds like you're carrying some worry at the moment.",
            "suggestion": "Take a few slow breaths and focus on what needs your attention right now."
        },
        {
            "message": "Feeling afraid can make the future seem overwhelming.",
            "suggestion": "Break the situation into smaller, manageable steps."
        }
    ],

    "surprise": [
        {
            "message": "That sounds like something you really didn't expect!",
            "suggestion": "Take a moment to process what happened and notice how you feel about it."
        },
        {
            "message": "It sounds like something caught you completely off guard.",
            "suggestion": "Give yourself some time to understand what happened before reacting."
        },
        {
            "message": "That seems like it came as quite a surprise.",
            "suggestion": "Think about whether the unexpected event changed how you feel about the situation."
        }
    ]
}


def get_wellbeing_response(emotion):
    emotion = emotion.lower()

    responses = EMOTION_RESPONSES.get(emotion)

    if responses:
        return random.choice(responses)

    return {
        "message": "I'm here to listen.",
        "suggestion": "Tell me a little more about how you're feeling."
    }