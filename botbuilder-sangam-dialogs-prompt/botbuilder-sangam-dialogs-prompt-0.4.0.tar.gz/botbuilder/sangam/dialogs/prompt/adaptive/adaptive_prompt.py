
from botbuilder.dialogs.prompts import Prompt, PromptOptions,PromptRecognizerResult
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes
from typing import Callable, Dict
import json

class AdaptiveCardPrompt(Prompt):
    def __init__(self, dialog_id: str, validator: object = None):
        super().__init__(dialog_id, validator=validator)

    async def on_prompt(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions, is_retry: bool):               
        if not turn_context:
            raise TypeError("turn_context Can’t  be none")
        if not options:
            raise TypeError("options Can’t  be none")

        if is_retry and options.retry_prompt is not None:
            await turn_context.send_activity(options.retry_prompt)
        else:
            if options.prompt is not None:
                await turn_context.send_activity(options.prompt)    
        
        return await super().on_prompt(turn_context, state, options, is_retry)

    async def on_recognize(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions):
        if not turn_context:
            raise TypeError("turn_context cannt be none")

        if not turn_context.activity:
            raise TypeError("turn_context.activity cannt be none")
        
        if turn_context.activity.type == ActivityTypes.message:
            usertext = turn_context.activity.value
            if usertext is not None:
                result = self.IsValidJson(usertext)
            else:
                result = False

            prompt_result = PromptRecognizerResult()
            prompt_result.succeeded = result

            if result == True:
                prompt_result.value = usertext                
            else:
                prompt_result.error = "Invalid JSON"

            return prompt_result               

    def IsValidJson(self,jsonString):
        try:
            json_data = json.dumps(jsonString)
            json.loads(json_data)
        except ValueError:
            return False
        return True
