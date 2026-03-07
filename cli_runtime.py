from google.genai import types
from google.genai.errors import ClientError
import prompts
from call_function import available_functions, call_function


def _process_conversation_turn(client, messages, working_directory, verbose=False):
    """
    Process a single conversation turn with the AI.
    Returns True if conversation should continue, False otherwise.
    """
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=prompts.system_prompt,
                    tools=[available_functions])
            )
        except Exception as e:
            if isinstance(e, ClientError):
                print('Ur out of tokens broke boy')
                return False

        if (response.candidates):
            for c in response.candidates:
                messages.append(c.content)

        if (response.usage_metadata is None):
            raise RuntimeError("Response is missing usage metadata")

        function_results = []

        if response.function_calls:
            for function_call in response.function_calls:
               function_call_result = call_function(function_call, working_directory, verbose)
               if not function_call_result.parts:
                   raise Exception('Parts property should be non null')
               if not function_call_result.parts[0].function_response:
                   raise Exception('Parts first response should be non null')
               if not function_call_result.parts[0].function_response.response:
                   raise Exception('Parts first response should be non null')

               function_results.append(function_call_result.parts[0])
               if verbose:
                   print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            if verbose:
                print('Prompt tokens: ' + str(response.usage_metadata.prompt_token_count))
                print('Response tokens: ' + str(response.usage_metadata.candidates_token_count))
            print('Response: ')
            print(response.text)
            return False

        messages.append(types.Content(role='user', parts=function_results))
    
    return True


def run_chatbot_loop(client, working_directory, verbose=False):
    """
    Run the interactive chatbot CLI.
    
    Args:
        client: Initialized Gemini API client
        working_directory: Directory to run file operations in
        verbose: Whether to print verbose output
    """
    print("Chatbot CLI (press Ctrl+C to exit)")
    print("-" * 40)
    
    try:
        while True:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            messages = [types.Content(role="user", parts=[types.Part(text=user_input)])]
            
            if verbose:
                print(f'User prompt: {user_input}')
            
            _process_conversation_turn(client, messages, working_directory, verbose)
    
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
