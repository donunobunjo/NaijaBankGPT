from app.graph import graph


result = graph.invoke(
    {
        "user_query": "My ATM card was declined.",
        "selected_language": "English",
    }
)


print("\n" + "=" * 60)
print("FINAL GRAPH STATE")
print("=" * 60)

print("Query:", result.get("user_query"))
print("Language:", result.get("selected_language"))
print("Is Banking:", result.get("is_banking"))
print("Intent:", result.get("intent"))
print(
    "Confidence:",
    result.get("intent_confidence"),
)
print("English Query:", result.get("english_query"))
print("Needs Clarification:", result.get("needs_clarification"))
print("Error:", result.get("error"))