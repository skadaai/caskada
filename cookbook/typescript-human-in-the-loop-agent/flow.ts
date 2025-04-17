import { Flow } from "brainyflow";
import { DecideNode, SearchNode, AnswerNode, ApprovalNode } from "./nodes";

export function createAgentFlow() {
    const decideNode = new DecideNode();
    const approvalNode = new ApprovalNode();
    const searchNode = new SearchNode();
    const answerNode = new AnswerNode();

    decideNode.on("search", approvalNode);
    approvalNode.on("search", searchNode);
    approvalNode.on("decide", decideNode)
    decideNode.on("answer", answerNode);
    searchNode.on("decide", decideNode);

    return new Flow(decideNode);
}
