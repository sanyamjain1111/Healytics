# Simple debug test to find the exact failure point

import google.generativeai as genai

# Your API key
API_KEY = "AIzaSyDJsa6J8hYaVnTVaJYKRcqZsgjHnFuxF90"

print("Step 1: Configuring API...")
try:
    genai.configure(api_key=API_KEY)
    print("✅ API configured successfully")
except Exception as e:
    print(f"❌ API configuration failed: {e}")
    exit(1)

print("\nStep 2: Creating model...")
try:
    model = genai.GenerativeModel("gemini-1.5-turbo")
    print("✅ Model created successfully")
    print(f"Model: {model}")
except Exception as e:
    print(f"❌ Model creation failed: {e}")
    exit(1)

print("\nStep 3: Testing simple generation...")
try:
    print("Calling generate_content...")
    resp = model.generate_content("Hello")
    print(f"✅ Got response object: {type(resp)}")
    print(f"Response object: {resp}")
except Exception as e:
    print(f"❌ generate_content failed: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\nStep 4: Accessing response text...")
try:
    text = resp.text
    print(f"✅ Response text: {text}")
except Exception as e:
    print(f"❌ Text access failed: {e}")
    print("Trying alternative access methods...")
    
    # Try to inspect the response object
    try:
        print(f"Response attributes: {dir(resp)}")
        if hasattr(resp, 'candidates'):
            print(f"Candidates: {resp.candidates}")
        if hasattr(resp, '_result'):
            print(f"Result: {resp._result}")
    except Exception as e2:
        print(f"Even inspection failed: {e2}")

print("\nStep 5: API Key validation...")
try:
    # Test if API key is valid by listing models
    models = list(genai.list_models())
    print(f"✅ API key is valid. Available models: {len(models)}")
    for model in models[:3]:  # Show first 3 models
        print(f"  - {model.name}")
except Exception as e:
    print(f"❌ API key validation failed: {e}")
    print("Your API key might be invalid, expired, or restricted.")