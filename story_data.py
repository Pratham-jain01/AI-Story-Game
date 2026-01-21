STORY_NODES = {
    "start": {
        "text": "The sun is setting. Your friend Rohan has a sprained ankle and cannot walk. A storm is visible on the horizon. What is your plan?",
        "target_intent": "The user should suggest staying with the friend, helping them move, or finding shelter together.",
        "success_node": "victory",
        "failure_node": "tragedy"
    },
    "victory": {
        "text": "Your loyalty saved him. You helped Rohan to a nearby cave and stayed warm. You win! Your friendship is stronger than ever.",
        "is_end": True
    },
    "tragedy": {
        "text": "You chose your own safety. Rohan was lost in the cold while you reached camp alone. Game over. You saved yourself, but lost a friend.",
        "is_end": True
    }
}
