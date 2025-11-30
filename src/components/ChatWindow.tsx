// src/components/ChatWindow.tsx

// ... (imports and useState/useRef declarations remain the same) ...

// Define the session ID for context management (can be static or generated once)
const SESSION_ID = 'user-session-123'; 

// --- UPDATED Function for calling the backend AI Agent ---
const callAgentApi = async (userInput: string): Promise<AgentResponse> => {
  // Replace with your actual backend URL (assuming it's running on port 8000)
  const API_URL = 'http://localhost:8000/chat'; 

  const requestBody = {
    user_input: userInput,
    session_id: SESSION_ID,
  };

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      // Handle HTTP errors (e.g., 404, 500)
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse the JSON response body
    const data = await response.json(); 
    
    // Map the FastAPI structure to the frontend structure
    const agentResponse: AgentResponse = {
      message: data.message,
      // Note: FastAPI uses snake_case (design_result_url), frontend uses camelCase (designResultUrl)
      designResultUrl: data.design_result_url, 
    };

    return agentResponse;

  } catch (error) {
    console.error("Error connecting to AI Agent backend:", error);
    // Re-throw a standardized error that the calling function can catch
    throw new Error('Failed to communicate with the AI agent.'); 
  }
};

// ... (The rest of the ChatWindow component remains the same) ...
