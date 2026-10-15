/**
 * Express REST Server for Task 2 — The Inbox Agent.
 * Runs on Port 8002.
 */

import express, { Request, Response } from 'express';
import path from 'path';
import { inboxAgent } from './inboxAgent';
import { EmailCategory } from './types';

const app = express();
const PORT = process.env.PORT || 8002;

app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'public')));

// List all emails with their current draft status
app.get('/api/emails', (req: Request, res: Response) => {
  const emails = inboxAgent.getEmails();
  const enhanced = emails.map(e => {
    const draft = inboxAgent.getDraft(e.id);
    return {
      ...e,
      draftStatus: draft ? draft.status : 'not_drafted',
      isAutonomous: draft ? draft.isAutonomous : false,
      draftPreview: draft ? draft.draftBody.slice(0, 120) + '...' : null
    };
  });
  res.json(enhanced);
});

// Helper to get string param
function getParamId(req: Request): string {
  const id = req.params.id;
  return Array.isArray(id) ? id[0] : id;
}

// Get single email and draft details
app.get('/api/emails/:id', (req: Request, res: Response) => {
  const emailId = getParamId(req);
  const email = inboxAgent.getEmailById(emailId);
  if (!email) return res.status(404).json({ error: 'Email not found' });
  const draft = inboxAgent.getDraft(emailId);
  res.json({ email, draft });
});

// Generate draft for email
app.post('/api/emails/:id/draft', async (req: Request, res: Response) => {
  const emailId = getParamId(req);
  try {
    const draft = await inboxAgent.generateDraft(emailId);
    res.json(draft);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// Human 1-click Approve and Send
app.post('/api/emails/:id/approve', (req: Request, res: Response) => {
  const emailId = getParamId(req);
  try {
    const result = inboxAgent.approveAndSend(emailId);
    res.json(result);
  } catch (err: any) {
    res.status(400).json({ error: err.message });
  }
});

// Human Edit and Send (Triggers self-learning loop + streak reset/circuit breaker)
app.post('/api/emails/:id/edit-send', (req: Request, res: Response) => {
  const emailId = getParamId(req);
  const { editedText, feedbackNotes } = req.body;
  if (!editedText) return res.status(400).json({ error: 'editedText is required' });

  try {
    const result = inboxAgent.editAndSend(emailId, editedText, feedbackNotes);
    res.json(result);
  } catch (err: any) {
    res.status(400).json({ error: err.message });
  }
});

// Graduation status and metrics per category
app.get('/api/graduation-status', (req: Request, res: Response) => {
  res.json(inboxAgent.getGraduationMetrics());
});

// List rules learned from human edits
app.get('/api/learned-rules', (req: Request, res: Response) => {
  res.json(inboxAgent.getLearnedRules());
});

// One-click simulation of 20 consecutive approvals for evaluator testing
app.post('/api/simulate-graduation', (req: Request, res: Response) => {
  const category = (req.body.category || 'how_to') as EmailCategory;
  const metrics = inboxAgent.simulateGraduation(category);
  res.json({
    message: `Simulated 20 consecutive approvals for category '${category}'. Category is now AUTONOMOUS.`,
    metrics
  });
});

app.listen(PORT, () => {
  console.log(`[Task 2] The Inbox Agent running on http://localhost:${PORT}`);
});
