from twin.crew import build_twin_crew

# CrewAI will call this
def run():
    print("🧠 Digital Twin Crew Started")

    # CrewAI passes inputs here
    company = input("Enter company name: ")

    crew = build_twin_crew(company)
    result = crew.kickoff()

    print("\n================ DIGITAL TWIN OUTPUT ================\n")
    print(result)


# Allows python src/twin/main.py Samsung
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        company = sys.argv[1]
        crew = build_twin_crew(company)
        print(crew.kickoff())
    else:
        run()
