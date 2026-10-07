"""Tool-calling practice: ask a local Ollama model questions about expense data.

Loads the transactions from ``expensetracker/data.csv`` and sends a question to
the model along with the tool schemas defined in
``llmpractice.toolcalling.agents.agent``. The script then runs the tool-calling
loop:

1. Send the conversation so far (plus the tool schemas) to the model.
2. If the model replies with plain text, print it and stop.
3. Otherwise, run each tool the model asked for against the loaded
   transactions, append the result as a ``tool`` message, and go back to 1.

The loop gives up after ``MAX_ROUNDS`` rounds, so a model that keeps asking for
tools cannot spin forever.

Rows that fail to load are reported on stderr and skipped.

Requires a running Ollama server with the ``llama3.1`` model pulled. Run from
the project root so the ``expensetracker`` package is importable:

    python -m llmpractice.toolcalling.main
"""

import json
import sys
from pathlib import Path

import ollama

from expensetracker.loader import load_transactions
from llmpractice.toolcalling.agents.agent import tools, tool_map

# Local Ollama model to chat with; it must support tool calling.
model = "llama3.1"

# Build the CSV path from this file's location so the script works from any cwd.
PROJECT_ROOT = Path(__file__).parent.parent.parent
data_path = PROJECT_ROOT / "expensetracker" / "data.csv"

# txns: the valid transactions; errors: one message per row that was rejected.
txns, errors = load_transactions(data_path)

for error in errors:
    print(f"Error: {error}", file=sys.stderr)

# Constrains the model to reporting tool output. Without this it happily derives
# figures itself, and generated arithmetic is wrong often enough to matter.
SYSTEM_PROMPT = (
    "You answer questions about the user's expense data, in Indian rupees.\n"
    "- Every number you report must come from a tool result. Never estimate, "
    "recall or work out a figure yourself.\n"
    "- If answering needs a value no tool returns, report what the tools do "
    "give you and say plainly that you cannot calculate the rest.\n"
    "- Do not describe the tools or your own reasoning; just answer."
)

# Conversation history. Every model reply and tool result is appended here, so
# each ollama.chat call sees the whole exchange so far.
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": "what is 15% of total income?"
    }
]

# Upper bound on model round-trips, so the loop always terminates.
MAX_ROUNDS = 5

for round_num in range(MAX_ROUNDS):
    # Passing `tools` lets the model answer with tool calls instead of text.
    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools
    )
    # Keep the model's reply (including any tool calls) in the history.
    messages.append(response.message)
    # No tool calls means this is the final answer.
    if not response.message.tool_calls:
        print(response.message.content)
        break
    # The model may ask for several tools in one reply; run each of them.
    for tool_call in response.message.tool_calls:
        tool_name = tool_call.function.name
        if tool_name not in tool_map:
            tool_resp = f"Error: no such tool {tool_name!r}"
        else:
            # Look up the Python function behind the tool name.
            tool = tool_map[tool_name]

            # The tools take no model-supplied arguments; they all work on the
            # transactions loaded above.
            tool_resp = tool(txns)

        # Send the result back as a "tool" message for the next round.


        messages.append(
            {
                "role": "tool",
                "content": json.dumps(tool_resp),
                "name": tool_name

            }
        )
else:
    print(f"No final answer after {MAX_ROUNDS} rounds.", file=sys.stderr)
