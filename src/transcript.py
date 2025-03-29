from smolagents import CodeAgent
import json

def summarize_transcripts(model, transcripts):
    transcript_agent = CodeAgent(
        tools=[],
        name="TranscriptSummariser",
        model=model,
        additional_authorized_imports=["json"],
        description="""Given a JSON file containing speeches from earnings call, generate a paragraph summarising their content using formal language.
        """
    )

    trans = {elem["content"] for elem in transcripts["transcript"]}
    
    result_summary = transcript_agent.run("Summarize the different transcripts from the earnings call, highlighting the most important aspects. The transcripts are given here:  " + str(trans))
    return result_summary