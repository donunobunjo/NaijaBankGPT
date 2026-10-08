from app.nodes.intent import BankingIntentClassifier


classifier = BankingIntentClassifier()


test_queries = [
    "My ATM card was declined.",
    "I want to know my account balance.",
    "I was charged twice for the same transaction.",
]


for query in test_queries:

    result = classifier.predict(query)

    print("\nQuery:")
    print(query)

    print("Intent:")
    print(result["intent"])

    print("Confidence:")
    print(round(result["confidence"], 4))