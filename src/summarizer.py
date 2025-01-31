from openai import OpenAI
import os
import logging

max_tokens = 16384

def summarize_text(text, max_tokens=max_tokens):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logging.error("OPENAI_API_KEY not found in environment variables!")
        raise ValueError("OPENAI_API_KEY must be set in environment variables")
    
    client = OpenAI(api_key=api_key)  
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that acts as a news reporter. Your task is to generate a report based on the provided content while adhering to the following guidelines: "
                       "1. Write exclusively in the third-person point of view. Avoid using second-person pronouns (e.g., 'you,' 'your') or addressing the reader directly. "
                       "2. Ensure the summary accurately conveys the key points, details, and nuances of the original content without altering their meaning. "
                       "3. Do not mention the original author, source, or article. Present the report as an independent explanation of the content. "
                       "4. Organize the report logically, grouping related ideas and themes, and highlight main topics, examples, and notable anecdotes. "
                       "5. Provide sufficient context to make the report understandable to someone unfamiliar with the original content. "
                       "6. Maintain a professional and informative tone, avoiding conversational language or attempts to engage the reader directly."
                },
                {
                    "role": "user",
                    "content": f"Generate a report according to the following text:\n{text}"
                }
            ],
            max_tokens=max_tokens,
            temperature=0.0
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    input_text = """
    What is pipelining?
Pipelining is a method of implementing and arranging data processing elements to allow the execution of multiple instructions concurrently by overlapping their execution. This requires thought in the design of hardware components and how they should be connected to enable pipeling efficiently.
If implemented succesfully, this improves efficiency, performance, and time consumption by breaking down tasks into smaller, independent stages.

Why is pipelining useful?
To show the motivation for pipelining, imagine a routine like doing laundry. We can abstract 4 steps for processing a load of dirty laundry.

Place dirty laundry in washer
When washer is finished, place laundry in dryer
When dryer is finished, place laundry on table to fold
When folding is finished, put clothes away
A simple approach would be to run through all steps, then repeat with a new load of clothes. This routine also takes a fixed time, because all stages can only proceed if the one before is completed.

However, if you have multiple loads of laundry at the same time, this can take a long time. And actually, there is room for improvement of the strategy above. If we observe the steps above, every component (washer, dryer, table) is used in only one step and is idle in 3 steps.
If we put a new load of clothes in the washer instantly after we unloaded it and move every load one step further, we can fill the idle time of every step and speed up the overall routine. And this without needing more machines or people!

What we achieve with this scheduling is improving the throughput of the routine by starting the routine another time if it is possible to initiate the first step again.
But we can observe some aspects of our pipeline to be considered:

The total time to complete the routine once does not change.
An improvement can be only achieved if there are separate resources for each stage.
The effective speed-up of doing laundry using pipelining is equal to the number of stages in the pipeline if all stages take about the same time and there is enough work to do.
E. g. 20 pipelined loads of laundry take about five times as long as 1 load, while 20 sequential loads would take 20 times as long as 1 load.
This means pipelined laundry is potentially four times faster than non-pipelined!
Pipelining applied to processors
Pipeling in processors means pipelining instruction executions. Analogously to laundry, we can divide the execution of a single instruction into steps, called stages.
The RISC-V instruction set is designed in a way that allows splitting every instruction execution into the same stages:
    """
    
    summary = summarize_text(input_text, max_tokens=max_tokens)
    print("Summary:", summary)
