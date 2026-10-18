# support_router.py

AUTO_REFUND_LIMIT = 1000
COMPLAINT_LIMIT = 3

def route_after_policy(state):
    # Rule 1: Check eligibility first. If false, route directly to explain the policy.
    if not state.get("eligible", False):
        return "explain_policy"
        
    # Rule 2: Check financial threshold limit constraints.
    if state.get("amount", 0) > AUTO_REFUND_LIMIT:
        return "human_review"
        
    # Rule 3: Check risk and customer complaint history frequencies.
    if state.get("refund_complaints", 0) >= COMPLAINT_LIMIT:
        return "human_review"
        
    # Rule 4: Default fallback path for safe, low-risk, automated approvals.
    return "issue_refund"

def human_review(state):
    """
    Executes the human escalation protocol. 
    Appends a standardized escalation notice to the state's final_answer.
    """
    order_id = state.get("order_id", "Unknown Order")
    amount = state.get("amount", 0)
    
    # Construct the personalized escalation notification message
    escalation_msg = (
        f"Refund request for order {order_id} (Amount: ${amount}) has been successfully flagged. "
        "A senior human support agent will manually review your transaction and reach out within 24 hours."
    )
    
    # Return a dictionary containing the state field update payload
    return {"final_answer": escalation_msg}

# Test Data Setup - Do not modify standard structures below
SAMPLE_STATES = [
    {"order_id": "R-101", "eligible": True,  "amount": 240,  "refund_complaints": 0},
    {"order_id": "R-102", "eligible": False, "amount": 900,  "refund_complaints": 0},
    {"order_id": "R-103", "eligible": True,  "amount": 2600, "refund_complaints": 0},
    {"order_id": "R-104", "eligible": True,  "amount": 300,  "refund_complaints": 4},
    {"order_id": "R-105", "eligible": False, "amount": 2800, "refund_complaints": 5},
    {"order_id": "R-106", "eligible": True,  "amount": 1000, "refund_complaints": 2},
]

if __name__ == "__main__":
    print("--- Support Agent Routing Logs ---")
    for state in SAMPLE_STATES:
        next_node = route_after_policy(state)
        print(f"{state['order_id']} -> {next_node}")

        # Execute the node function
        state_updates = human_review(state)
    
        # Print the resulting payload that updates the state graph ledger
        print("Returned State Update Payload:")
        import json
        print(json.dumps(state_updates, indent=4))
