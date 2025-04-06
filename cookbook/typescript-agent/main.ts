import { createAgentFlow } from "./flow";
import { SearchAgentSharedContext } from "./nodes";

async function main() {
    const question = process.argv[2] || "who is the ceo of microsoft?";
    const agentFlow = createAgentFlow();
    const sharedContext: SearchAgentSharedContext = {
        question: question,
    }
    await agentFlow.run(sharedContext);
}

main().catch((error) => {
    console.error("Error running the agent:", error);
});
