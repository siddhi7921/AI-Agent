const callAgentApi = async (userInput: string, timeout = 10000): Promise<AgentResponse> => {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_input: userInput, session_id: SESSION_ID }),
      signal: controller.signal,
    });

    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    return { message: data.message, designResultUrl: data.design_result_url };
  } catch (error) {
    console.error("Error connecting to AI Agent backend:", error);
    throw new Error('Failed to communicate with the AI agent.');
  } finally {
    clearTimeout(id);
  }
};

