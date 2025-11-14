import google.generativeai as genai
from dotenv import load_dotenv
import os

def test_gemini_api():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        return False
    
    print(f"✅ Found API Key: {api_key[:10]}...{api_key[-10:]}")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Use the available Gemini 2.5 models
        model_names = [
            "gemini-2.5-flash",  # Stable version
            "gemini-2.5-flash-preview-05-20",  # Preview version
            "gemini-2.5-pro-preview-03-25"  # Pro preview
        ]
        
        for model_name in model_names:
            try:
                print(f"🔧 Testing model: {model_name}")
                
                # Initialize the model
                model = genai.GenerativeModel(model_name)
                
                # Test with a simple prompt
                response = model.generate_content("Say 'Hello, Gemini API is working!' in a creative way.")
                
                print(f"✅ SUCCESS with {model_name}!")
                print(f"📝 Response: {response.text}")
                print("\n🎉 Gemini API is working correctly!")
                return True
                
            except Exception as e:
                print(f"❌ Failed with {model_name}: {e}")
                continue
        
        print("❌ All model attempts failed")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api()