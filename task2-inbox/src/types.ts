/**
 * Core type definitions for Task 2 — The Inbox Agent.
 * Enforces strict typing across emails, drafting, self-learning, and graduation.
 */

export type EmailCategory = 
  | 'how_to'
  | 'refund_cancellation'
  | 'new_project_request'
  | 'complaint'
  | 'quote'
  | 'follow_up'
  | 'edge_cases';

export interface CustomerEmail {
  id: string;
  sender: string;
  subject: string;
  body: string;
  category: EmailCategory;
  received_at: string;
}

export interface CitedKnowledgeSource {
  id: string;
  title: string;
  url: string;
  category: string;
  folder: string;
  relevance_score: number;
}

export interface EmailDraft {
  emailId: string;
  category: EmailCategory;
  draftBody: string;
  confidence: number;
  sources: CitedKnowledgeSource[];
  isAutonomous: boolean;
  status: 'pending_review' | 'approved_sent' | 'edited_sent' | 'rejected_escalated';
  originalDraft?: string;
  humanEditedDraft?: string;
  sentAt?: string;
  feedbackNotes?: string;
}

export interface LearnedRule {
  id: string;
  category: EmailCategory;
  ruleTitle: string;
  instruction: string;
  triggerPhrase: string;
  learnedFromEmailId: string;
  createdAt: string;
}

export interface CategoryGraduationMetrics {
  category: EmailCategory;
  consecutiveUneditedApprovals: number;
  graduationThreshold: number; // 20 required
  isAutonomous: boolean;
  totalDrafted: number;
  totalApprovedUnedited: number;
  totalEditedByHuman: number;
  totalRejected: number;
  lastGraduatedAt?: string;
  lastDegradedAt?: string;
  degradationReason?: string;
}

export interface KnowledgeBrainResponse {
  answer: string;
  confidence: number;
  sources: CitedKnowledgeSource[];
  escalated: boolean;
  escalation_id?: string;
  honest_abstention: boolean;
}

export interface CapabilityCheckResponse {
  classification: 'NATIVE_SETTING' | 'STANDARD_CUSTOMIZATION' | 'COMPLEX_CUSTOM_DEV';
  confidence: number;
  is_native: boolean;
  setting_location: string;
  recommended_action: string;
  estimated_hours: number;
  cost_to_client: number;
  savings_vs_custom: number;
  source_article?: {
    id: string;
    title: string;
    url: string;
  };
}
