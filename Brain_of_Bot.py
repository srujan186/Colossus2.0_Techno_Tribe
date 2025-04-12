import os
import base64
import logging
from groq import Groq

# Set default model
DEFAULT_MODEL = "llama-3.2-90b-vision-preview"

# Setup logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

def encode_image(image_path):
    """
    Encode an image file as base64 string.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        str: Base64 encoded image string.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error encoding image {image_path}: {e}")
        return None

def analyze_image_with_query(query, model=DEFAULT_MODEL, encoded_image=None):
    """
    Analyze an image with a text query using Groq's vision model.
    
    Args:
        query (str): User's text query about the image.
        model (str): Model ID to use for analysis.
        encoded_image (str): Base64 encoded image string.
        
    Returns:
        str: AI-generated response to the query about the image.
    """
    # Log function call
    logging.info(f"Analyzing image with query: {query[:50]}...")
    logging.info(f"Using model: {model}")
    
    # Get API key from environment
    groq_api_key = os.environ.get("GROQ_API_KEY")
    
    if not groq_api_key:
        logging.error("GROQ_API_KEY environment variable not set")
        return "Error: GROQ_API_KEY environment variable not set."
        
    if not encoded_image:
        logging.error("No image provided for analysis")
        return "Error: No image provided for analysis."
    
    # Truncate image string for logging to avoid overwhelming logs
    image_snippet = encoded_image[:30] + "..." if encoded_image else "None"
    logging.info(f"Image data received (snippet): {image_snippet}")
    
    try:
        # Initialize Groq client with API key
        client = Groq(api_key=groq_api_key)
        logging.info("Groq client initialized")
        
        # Incorporate the system prompt into the user message instead
        # Since Groq API doesn't allow both system messages and images
        enhanced_query = (
            "You are a professional dermatologist AI. Based on my skin image and the following query, tell what skin disease user might have using image and query "
            "provide an accurate and empathetic recommendation. Explain clearly in simple language. "
            "If the issue seems serious or unclear, advise consulting a dermatologist in person.\n\n"
            f"My query: {query}"
        )
        
        logging.info(f"Enhanced query prepared: {enhanced_query[:50]}...")
        
        # Prepare messages without system role
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": enhanced_query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }
        ]
        
        logging.info("Making API call to Groq...")
        
        # Make API call
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model
            )
            logging.info("Received response from Groq API")
            
            # Log a short preview of the response for debugging
            response_content = chat_completion.choices[0].message.content
            logging.info(f"Response preview: {response_content[:100]}...")
            
            return response_content
            
        except Exception as api_error:
            logging.error(f"API call error: {type(api_error).__name__}: {str(api_error)}")
            return f"Error calling Groq API: {str(api_error)}"
        
    except Exception as e:
        logging.error(f"General error: {type(e).__name__}: {str(e)}")
        return f"Error during analysis: {str(e)}"
