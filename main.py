from agents.agent_runner import run_agent

if __name__=="__main__":
    print("Welcome to PrescriptionAI")
    while True:
        user_input = input("\nAsk your medical question (or type 'exit'):")
        if user_input.lower()=='exit':
            break
        response=run_agent(user_input)
        print("Assistant:\n", response)
