def interest_scoring(user_interests, club_interests):
    """Return the share of selected interests present in a club's tags."""
    if not user_interests:
        return 1.0

    selected = set(user_interests)
    available = set(club_interests)
    return len(selected & available) / len(selected)


def combine_scores(semantic_score, interest_score, semantic_weight=0.7):
    """Combine semantic and interest signals using an explicit weight."""
    if not 0 <= semantic_weight <= 1:
        raise ValueError("semantic_weight must be between 0 and 1")
    return semantic_score * semantic_weight + interest_score * (1 - semantic_weight)
