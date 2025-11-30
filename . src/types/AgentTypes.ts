// src/types/AgentTypes.ts

/**
 * Who sent the message
 */
export type MessageRole = 'user' | 'agent' | 'system';

/**
 * A single message in the chat
 */
export interface AgentMessage {
  /** Unique ID for message */
  id: string;

  /** Sender of the message (user/agent/system) */
  role: MessageRole;

  /** Text content of the message */
  content: string;

  /**
   * Optional visual output (image, design, chart, etc.)
   * Example: URL from an AI-generated design output
   */
  visualOutputUrl?: string;
}

/**
 * Raw response returned by the AI agent or backend function
 */
export interface AgentResponse {
  /** The message the AI generates */
  message: string;

  /**
   * Optional generated design URL
   * Example: https://cdn.vercel.com/designs/xyz123.png
   */
  designResultUrl?: string;
}
