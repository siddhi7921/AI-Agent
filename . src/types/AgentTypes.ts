// src/types/AgentTypes.ts

export type MessageRole = 'user' | 'agent' | 'system';

export interface AgentMessage {
  id: string;
  role: MessageRole;
  content: string;
  // Optional field to hold visual output (e.g., a URL to the generated design)
  visualOutputUrl?: string; 
}

export interface AgentResponse {
  message: string;
  // This is the key: if the response is a design, it includes the URL
  designResultUrl?: string; 
}
