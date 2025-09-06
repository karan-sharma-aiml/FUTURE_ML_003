import openai
from transformers import pipeline
from rasa.core.agent import Agent
from backend.config import OPENAI_API_KEY, HF_API_TOKEN
from backend.memory import update_memory, get_memory

# Configure OpenAI API key
openai.api_key = OPENAI_API_KEY

# Configure Hugging Face generator fallback with PyTorch backend
generator = pipeline(
    "text-generation",
    model="EleutherAI/gpt-neo-125M",
    framework="pt",            # Added to force PyTorch backend
    use_auth_token=HF_API_TOKEN
)

# Load entire Rasa agent (includes NLU + Core)
agent = Agent.load("./rasa_bot/models/20250902-140752-intense-wattage.tar.gz")

async def rasa_response_async(user_input):
    responses = await agent.handle_text(user_input)
    if responses:
        first = responses[0]
        intent = first.get("intent", {}).get("name", "")
        confidence = first.get("intent", {}).get("confidence", 0.0)
        return intent, confidence
    return "", 0.0

def rasa_response(user_input):
    import asyncio
    return asyncio.run(rasa_response_async(user_input))

def gpt_fallback(user_input, history):
    prompt = "\n".join([h["bot"] for h in history] + [user_input])
    if OPENAI_API_KEY:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[*history, {"role":"user","content":user_input}]
        )
        return response["choices"][0]["message"]["content"]
    outputs = generator(prompt, max_length=200, do_sample=True)
    return outputs[0]["generated_text"]

def get_bot_response(user_id, user_input):
    history = [{"role": "assistant", "content": h["bot"]} for h in get_memory(user_id)]
    intent, confidence = rasa_response(user_input)
    if confidence > 0.7:
        response = f"Detected intent: {intent}. (Rasa handled)"
    else:
        response = gpt_fallback(user_input, history)
    update_memory(user_id, user_input, response)
    return response
