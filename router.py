def route_query(user_query: str) -> str:
    """
    Route the user query to the appropriate tool based on keywords.
    Returns a string indicating which tool to use.
    """
    query_lower = user_query.lower()
    if "return" in query_lower or "policy" in query_lower :
        return "policy_agent"
    elif "order" in query_lower or "tracking" in query_lower:
        return "sql_agent"
    elif "hate" in query_lower or "angry" in query_lower or "human" in query_lower:
        return "human_escalation"
    else:
        return "general_chat"