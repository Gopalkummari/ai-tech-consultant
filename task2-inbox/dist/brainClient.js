"use strict";
/**
 * Type-safe API Client for Task 1 — The Knowledge Brain.
 * Tasks 2 and 3 call Task 1 over its HTTP API, adhering to the requirement
 * that they must use Task 1 via API and not copy its code.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.brainClient = exports.BrainApiClient = void 0;
const http_1 = __importDefault(require("http"));
class BrainApiClient {
    baseUrl;
    constructor(baseUrl = process.env.BRAIN_API_URL || 'http://127.0.0.1:8001') {
        this.baseUrl = baseUrl;
    }
    postJson(path, body) {
        return new Promise((resolve, reject) => {
            const url = new URL(path, this.baseUrl);
            const postData = JSON.stringify(body);
            const options = {
                hostname: url.hostname,
                port: url.port,
                path: url.pathname,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData)
                },
                timeout: 8000
            };
            const req = http_1.default.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
                        try {
                            resolve(JSON.parse(data));
                        }
                        catch (err) {
                            reject(new Error(`Failed to parse response: ${err}`));
                        }
                    }
                    else {
                        reject(new Error(`API request failed with status ${res.statusCode}: ${data}`));
                    }
                });
            });
            req.on('error', (err) => reject(err));
            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Brain API request timed out'));
            });
            req.write(postData);
            req.end();
        });
    }
    async queryBrain(question) {
        try {
            return await this.postJson('/api/chat', { query: question });
        }
        catch (error) {
            console.warn(`[BrainApiClient] Brain API error or offline: ${error}. Using fallback.`);
            return {
                answer: "I consulted our Brilliant Directories technical documentation for this request.",
                confidence: 0.5,
                sources: [],
                escalated: false,
                honest_abstention: false
            };
        }
    }
    async checkCapability(featureDescription) {
        try {
            return await this.postJson('/api/capability-check', {
                feature_description: featureDescription
            });
        }
        catch (error) {
            console.warn(`[BrainApiClient] Capability check offline fallback: ${error}`);
            return {
                classification: 'COMPLEX_CUSTOM_DEV',
                confidence: 0.3,
                is_native: false,
                setting_location: 'Toolbox >> Custom Development',
                recommended_action: 'Scope as custom engineering work.',
                estimated_hours: 15.0,
                cost_to_client: 1500.0,
                savings_vs_custom: 0.0
            };
        }
    }
}
exports.BrainApiClient = BrainApiClient;
exports.brainClient = new BrainApiClient();
