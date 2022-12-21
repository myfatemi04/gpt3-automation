import llms

assistant = llms.CompletionPrompt("""
Platform: MacOS
Shell: /bin/bash
Assistant is a tool that interacts with the command line to perform tasks for the user.
Assistant can execute commands by writing "Execute: <command goes here>".
Assistant can also ask questions to the user before running a command.
Assistant can write computer programs by echoing the lines of each program in sequence.
If Assistant believes it cannot do something, it will ask the user for permission.
Assistant can use the command "python bing_search.py <query>" to find a list of pages.
Assistant can parse the text of a URL with "./parse_text_from_url.sh <url>".
Assistant can use "curl" for other API calls.
User cannot directly see command line output. User can only see text in "Assistant:" sections, not in "Command line" sections.

Example 1:
User: Is IPython installed?
Assistant: Execute: pip3 freeze | grep ipython
Command line (Only seen by Assistant):
```
ipython==7.16.1
```
(stderr omitted)
```
Assistant: IPython is installed, and is version 7.16.1.

Example 2:
User: Parse the text at the url "https://www.google.com/".
Assistant: Execute: ./parse_text_from_url.sh https://www.google.com/
Command line (Only seen by Assistant):
```
(output omitted)
```
(stderr omitted)
```
Assistant: The text at the url is (text omitted)

Begin.
{past_context}
Assistant:
""".strip(), generation_params={"temperature": 0.5, "max_tokens": 256, "stop": ["\nCommand", "\nAssistant", "\nUser"]})

import subprocess
import os

def run_and_return_stdout_and_stderr_in_one_string(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode("utf-8"), stderr.decode("utf-8")

def loop():
    past_context = ""
    skip_user = False
    while True:
        if not skip_user:
            user_input = input("User: ")
            past_context += "User: " + user_input + "\n"

        result = assistant(past_context=past_context[
            -8000:
        ]).strip()
        skip_user = False
        print("Assistant:", result, "\n")
        past_context += "Assistant: " + result + "\n"

        cmd = None
        if "Execute: " in result:
            cmd = result[result.index("Execute: ") + 9:]
        elif "Executing: " in result:
            cmd = result[result.index("Executing: ") + 11:]
        if cmd:
            print("Command:", cmd)
            stderr = ""
            stdout = ""
            if cmd.startswith("nano ") or cmd.startswith("vi "):
                stderr = "ERROR: Assistant cannot use Nano or Vi. Assistant will use a series of \"echo\" commands to achieve a similar result."
            else:
                try:
                    import time
                    start_time = time.time()
                    stdout, stderr = run_and_return_stdout_and_stderr_in_one_string(cmd)
                    end_time = time.time()
                except KeyboardInterrupt:
                    stderr = "<User interrupted the command. Execution time: " + str(end_time - start_time) + " seconds.>"
            print("Command line (Only seen by Assistant):")
            print(stdout[-1000:])
            print(stderr[-1000:])
            past_context += "Command line (Only seen by Assistant):\n```\n" + stdout[-1000:] + "\n```\n" + stderr[-1000:] + "\n```\n"
            skip_user = True

loop()
