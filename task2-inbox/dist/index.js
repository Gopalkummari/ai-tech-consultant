"use strict";
/**
 * Express REST Server for Task 2 — The Inbox Agent.
 * Runs on Port 8002.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const path_1 = __importDefault(require("path"));
const inboxAgent_1 = require("./inboxAgent");
const app = (0, express_1.default)();
const PORT = process.env.PORT || 8002;
app.use(express_1.default.json());
app.use(express_1.default.static(path_1.default.join(__dirname, '..', 'public')));
// List all emails with their current draft status
app.get('/api/emails', (req, res) => {
    const emails = inboxAgent_1.inboxAgent.getEmails();
    const enhanced = emails.map(e => {
        const draft = inboxAgent_1.inboxAgent.getDraft(e.id);
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
function getParamId(req) {
    const id = req.params.id;
    return Array.isArray(id) ? id[0] : id;
}
// Get single email and draft details
app.get('/api/emails/:id', (req, res) => {
    const emailId = getParamId(req);
    const email = inboxAgent_1.inboxAgent.getEmailById(emailId);
    if (!email)
        return res.status(404).json({ error: 'Email not found' });
    const draft = inboxAgent_1.inboxAgent.getDraft(emailId);
    res.json({ email, draft });
});
// Generate draft for email
app.post('/api/emails/:id/draft', async (req, res) => {
    const emailId = getParamId(req);
    try {
        const draft = await inboxAgent_1.inboxAgent.generateDraft(emailId);
        res.json(draft);
    }
    catch (err) {
        res.status(500).json({ error: err.message });
    }
});
// Human 1-click Approve and Send
app.post('/api/emails/:id/approve', (req, res) => {
    const emailId = getParamId(req);
    try {
        const result = inboxAgent_1.inboxAgent.approveAndSend(emailId);
        res.json(result);
    }
    catch (err) {
        res.status(400).json({ error: err.message });
    }
});
// Human Edit and Send (Triggers self-learning loop + streak reset/circuit breaker)
app.post('/api/emails/:id/edit-send', (req, res) => {
    const emailId = getParamId(req);
    const { editedText, feedbackNotes } = req.body;
    if (!editedText)
        return res.status(400).json({ error: 'editedText is required' });
    try {
        const result = inboxAgent_1.inboxAgent.editAndSend(emailId, editedText, feedbackNotes);
        res.json(result);
    }
    catch (err) {
        res.status(400).json({ error: err.message });
    }
});
// Graduation status and metrics per category
app.get('/api/graduation-status', (req, res) => {
    res.json(inboxAgent_1.inboxAgent.getGraduationMetrics());
});
// List rules learned from human edits
app.get('/api/learned-rules', (req, res) => {
    res.json(inboxAgent_1.inboxAgent.getLearnedRules());
});
// One-click simulation of 20 consecutive approvals for evaluator testing
app.post('/api/simulate-graduation', (req, res) => {
    const category = (req.body.category || 'how_to');
    const metrics = inboxAgent_1.inboxAgent.simulateGraduation(category);
    res.json({
        message: `Simulated 20 consecutive approvals for category '${category}'. Category is now AUTONOMOUS.`,
        metrics
    });
});
app.listen(PORT, () => {
    console.log(`[Task 2] The Inbox Agent running on http://localhost:${PORT}`);
});
